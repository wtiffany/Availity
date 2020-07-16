import React, { Component } from 'react';
import { Scope } from '@unform/core';
import { Form } from '@unform/web';
import Input from './components/Input';
import './App.css';

export class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			value: 'Submitted values will appear here',
		};
	}

	handleSubmit = (data, { reset }) => {
		this.setState({ value: JSON.stringify(data) });
		reset();
	};

	render() {
		return (
			<div>
				<Form onSubmit={this.handleSubmit}>
					<img src='https://prnewswire2-a.akamaihd.net/p/1893751/sp/189375100/thumbnail/entry_id/0_ibyy2qeg/def_height/838/def_width/1600/version/100012/type/2/q/100' height='150' width='175' alt='Unform' />

					<Input name='name' label='Full Name' />
					<Input name='npi' label='NPI Number' type='npi' />
					<Scope path='address'>
						<Input name='street' label='Business Street Name' />
						<Input name='zipcode' label='ZIP Code' />
					</Scope>
					<Input name='telephone' label='Telephone Number' type='telephone' />
					<Input name='email' label='E-mail' type='email' />

					<button type='submit'>Save</button>
					<br></br>
					<textarea value={this.state.value} rows='6' readOnly></textarea>
				</Form>
			</div>
		);
	}
}

export default App;
