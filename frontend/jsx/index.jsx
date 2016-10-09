import React from 'react';
import ReactDOM from 'react-dom';

import AppBar from 'components/app-bar';
import ContactList from 'components/contact-list';

class Application extends React.Component {
	render() {
		return (
			<div className="application-component">
				<AppBar />
				<ContactList />
			</div>
		);
	}
}

ReactDOM.render(
	<Application />,
	document.getElementById("content")
);
