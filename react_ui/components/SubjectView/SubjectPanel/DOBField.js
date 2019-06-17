import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import DatePicker from 'react-datepicker';


<DatePicker
    selected={this.state.startDate}
    onChange={this.handleChange}
    peekNextMonth
    showMonthDropdown
    showYearDropdown
    dropdownMode="select"
/>
