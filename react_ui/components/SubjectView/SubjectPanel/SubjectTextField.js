import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import TextField from '@material-ui/core/TextField';
import * as SubjectActions from '../../../actions/subject';

class SubjectTextField extends React.Component {

  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  onChange(e) {
    // Check to see if we're editing an existing subject
    if (!this.props.new) {
      // Changing the input fields should update the state of the active subject
      const sub = this.props.subject;
      sub[this.props.skey] = e.target.value.trim();
      this.props.dispatch(SubjectActions.setActiveSubject(sub));
    } else {
      const sub = this.props.newSubject;
      sub[this.props.skey] = e.target.value.trim();
    }
  }

  render() {
    let style = {};
    if (this.props.error) {
        style = {backgroundColor: 'pink'};
    }

    return (
      <div className="form-group">
        <label htmlFor="formGroupExampleInput">{this.props.label}</label>
          <input
            type="text"
            className="form-control"
            id="formGroupExampleInput"
            onChange={this.onChange}
            style= {style}
            value={this.props.value}
          />
       {this.props.error
      ? <p> {this.props.error} </p>
    : null  }
    </div>
    );
  }
}

SubjectTextField.propTypes = {
  dispatch: PropTypes.func,
  new: PropTypes.bool,
  subject: PropTypes.object,
  newSubject: PropTypes.object,
  skey: PropTypes.string,
  value: PropTypes.string,
  error: PropTypes.string,
  label: PropTypes.string,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    newSubject: state.subject.newSubject,
  };
}

export default connect(mapStateToProps)(SubjectTextField);
