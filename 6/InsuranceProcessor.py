import collections
import os
import unittest


class InsuranceProcessor:
    def __init__(self, filename=None):
        self.id_to_record = {}
        if filename is not None:
            # Open the file and convert its contents into InsuranceRecord objects.
            with open(filename, "r") as f:
                for csv_string in f.readlines():
                    self.addInsuranceRecord(csv_string)

    def addInsuranceRecord(self, csv_string):
        record = InsuranceRecord(csv_string.strip())
        # This user was seen before. Only overwrite if it is a newer version.
        if record.user_id in self.id_to_record:
            existing_record = self.id_to_record[record.user_id]
            if record.version < existing_record.version:
                # Return, as the existing record is newer.
                return
        # If there is no existing record, or the existing record is older, add
        # the record to the record map.
        self.id_to_record[record.user_id] = record

    def populateInsuranceToRecords(self):
        self.insurance_to_records = collections.defaultdict(list)
        # Group everything by insurance company
        for record in self.id_to_record.values():
            self.insurance_to_records[record.insurance_company].append(record)

        # Sort by first and last name.
        for insurance_company, records in self.insurance_to_records.items():
            self.insurance_to_records[insurance_company].sort(
                key=lambda x: (x.last_name, x.first_name))

    def writeToFiles(self):
        self.populateInsuranceToRecords()
        for insurance_company in self.insurance_to_records:
            with open("%s.csv" % insurance_company, 'w') as f:
                for record in self.insurance_to_records[insurance_company]:
                    f.write(record.__str__() + "\n")


class InsuranceRecord:
    def __init__(self, csv_string):
        self.user_id, self.name, self.version, self.insurance_company = \
            csv_string.split(",")
        self.first_name, self.last_name = self.name.split(" ")
        self.version = int(self.version)

    def __eq__(self, other):
        return self.user_id == other.user_id and self.name == other.name and \
            self.version == other.version and self.insurance_company == other.insurance_company

    def __str__(self):
        return "%s,%s,%d,%s" % \
            (self.user_id, self.name, self.version, self.insurance_company)


class UnitTests(unittest.TestCase):
    def test_shouldAddRecord(self):
        # Define test constants
        user_id = "user_id_1"
        first_and_last_name = "Jon Snow"
        insurance_company_1 = "Insurance Co 1"

        # Construct processor instance
        processor = InsuranceProcessor()

        # Add records to the processor
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id, first_and_last_name, 1, insurance_company_1))

        # Extract record given the user id
        record = processor.id_to_record[user_id]

        # Assert it is the record that we are expecting
        self.assertEqual(record.name, first_and_last_name)
        self.assertEqual(record.insurance_company, insurance_company_1)
        self.assertEqual(record.version, 1)

    def test_shouldOnlyKeepMostRecentVersion(self):
        # Define test constants
        user_id = "user_id_1"
        first_and_last_name = "Jon Snow"
        insurance_company_1 = "Insurance Co 1"
        insurance_company_2 = "Insurance Co 2"
        insurance_company_3 = "Insurance Co 3"

        # Construct processor instance
        processor = InsuranceProcessor()

        # Add records to the processor
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id, first_and_last_name, 1, insurance_company_1))
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id, first_and_last_name, 3, insurance_company_3))
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id, first_and_last_name, 2, insurance_company_2))

        # Extract record given the user id
        record = processor.id_to_record[user_id]

        # Assert it is the record that we are expecting
        self.assertEqual(record.name, first_and_last_name)
        self.assertEqual(record.insurance_company, insurance_company_3)
        self.assertEqual(record.version, 3)

    def test_shouldGroupByInsuranceCompany(self):
        # Define test constants
        user_id_1 = "user_id_1"
        user_id_2 = "user_id_2"
        user_id_3 = "user_id_3"
        user_id_4 = "user_id_4"
        first_and_last_name_1 = "The Hound"
        first_and_last_name_2 = "Tyrion Lannister"
        first_and_last_name_3 = "Jon Snow"
        first_and_last_name_4 = "Jamie Lannister"
        insurance_company_1 = "Insurance Co 1"

        # Construct processor instance
        processor = InsuranceProcessor()

        # Add records to the processor
        # These records will be added to insurance company 1
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id_1, first_and_last_name_1, 1, insurance_company_1))
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id_2, first_and_last_name_2, 2, insurance_company_1))
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id_3, first_and_last_name_3, 3, insurance_company_1))
        processor.addInsuranceRecord("%s,%s,%d,%s" % (
            user_id_4, first_and_last_name_4, 4, insurance_company_1))

        # Populate the insurance to record map.
        processor.populateInsuranceToRecords()

        self.assertEqual(len(processor.insurance_to_records), 1)
        # Assert that we are sorting by last name, then first name. This is in ascending order, meaning the first
        # record will be lexicographically the latest. The last record will be lexicographically the first.
        self.assertListEqual(processor.insurance_to_records[insurance_company_1],
                             [
                                 # The Hound
                                 InsuranceRecord("%s,%s,%d,%s" % (
                                     user_id_1, first_and_last_name_1, 1, insurance_company_1)),
                                 # Jamie Lannister is before Tyrion because J is in ascending order from T.
                                 InsuranceRecord("%s,%s,%d,%s" % (
                                     user_id_4, first_and_last_name_4, 4, insurance_company_1)),
                                 # Tyrion Lannister
                                 InsuranceRecord("%s,%s,%d,%s" % (
                                     user_id_2, first_and_last_name_2, 2, insurance_company_1)),
                                 # Jon Snow
                                 InsuranceRecord("%s,%s,%d,%s" % (
                                     user_id_3, first_and_last_name_3, 3, insurance_company_1))
        ])

    def test_shouldPopulateFromFile(self):
        # Construct processor instance
        processor = InsuranceProcessor("test.csv")

        # Assert that we read in all of the records.
        self.assertEqual(len(processor.id_to_record), 36)

    def test_shouldWriteOutToFile(self):
        # Construct processor instance
        processor = InsuranceProcessor("test.csv")
        processor.writeToFiles()

        # Assert that we read in all of the records.
        self.assertTrue(os.path.isfile("co_1.csv"))
        self.assertTrue(os.path.isfile("co_2.csv"))
        self.assertTrue(os.path.isfile("co_3.csv"))


if __name__ == "__main__":
    # Change the directory to the directory containing this file.
    os.chdir(os.path.dirname(__file__))
    unittest.main()
