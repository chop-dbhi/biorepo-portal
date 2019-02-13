import React from 'react';
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
    let errorText = '';
    if (this.props.error) {
      errorText = 'This field is required.';
    }

    return (
      <TextField
        onChange={this.onChange}
        style={{ width: '100%', whiteSpace: 'nowrap' }}
        value={this.props.value}
        floatingLabelText={this.props.label}
        errorText={errorText}
      />
    );
  }
}

SubjectTextField.propTypes = {
  dispatch: React.PropTypes.func,
  new: React.PropTypes.bool,
  subject: React.PropTypes.object,
  newSubject: React.PropTypes.object,
  skey: React.PropTypes.string,
  value: React.PropTypes.string,
  error: React.PropTypes.string,
  label: React.PropTypes.string,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    newSubject: state.subject.newSubject,
  };
}

export default connect(mapStateToProps)(SubjectTextField);
