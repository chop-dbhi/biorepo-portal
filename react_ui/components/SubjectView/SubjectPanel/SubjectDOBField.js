import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import DatePicker from 'react-datepicker';
import moment from 'moment';

import 'react-datepicker/dist/react-datepicker.css';
import 'react-datepicker/dist/react-datepicker-cssmodules.css';

class SubjectDOBField extends React.Component {

  constructor(props) {
    super(props);
    this.state={value: ''};
    this.onChange = this.onChange.bind(this);
  }

  onChange(e) {
    const sub = this.props.newSubject;
    let date= moment(e);

    this.setState({value: e});
    sub.dob = date.format('YYYY-MM-DD');

  }

  render() {
    let errorText = '';
    if (this.props.error) {
      errorText = 'This field is required.';
    }
    return (

        <div className="form-group">
          <h5 className="category" style={{fontWeight: "bold"}} > Date of Birth (YYYY-MM-DD) </h5>
          <DatePicker
              selected={this.state.value}
              onChange={this.onChange}
              peekNextMonth
              showMonthDropdown
              showYearDropdown
              scrollableYearDropdown
              dropdownMode="select"
              dateFormat="yyyy-MM-dd"
          />
        </div>

    );
  }
}

SubjectDOBField.propTypes = {
  dispatch: PropTypes.func,
  value: PropTypes.string,
  error: PropTypes.string,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    newSubject: state.subject.newSubject,
  };
}

export default connect(mapStateToProps)(SubjectDOBField);
