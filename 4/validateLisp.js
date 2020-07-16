// Coding exercise: You are tasked to write a checker that validates the parentheses of a LISP code.  Write a program (in Java or JavaScript) which takes in a string as an input and returns true if all the parentheses in the string are properly closed and nested.


function validateLisp(str) {
  var depth = 0;
  for (var i = 0; i < str.length; i++) {
    if (str[i] === "(") {
      depth++;
    } else if (str[i] === ")") {
      if (depth === 0) {
        return false;
      }
      depth--;
    }
  }
  return depth === 0;
}

console.assert(validateLisp("(defun triple (X)(* 3 X))"), "Valid lisp test case")
console.assert(validateLisp("(defun triple (X)(* 3 X)))") === false, "Too many closing parentheses test case")
console.assert(validateLisp("((defun triple (X)(* 3 X))" === false), "Too many opening parentheses test case")
console.log("All tests finished running.")