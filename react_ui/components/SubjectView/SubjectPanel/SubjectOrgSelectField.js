import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
// import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import * as SubjectActions from '../../../actions/subject';
import Select from 'react-select';


class SubjectOrgSelectField extends React.Component {
  constructor(props) {
    super(props);
    this.state = { value: '',};
    this.onChange = this.onChange.bind(this);
  }

  orgOptions(){
    let orgList = null;
    let orgs = this.props.orgs
    orgList = orgs.map(org => ({
      value: org.id,
      label: org.name,
    }));
    return orgList
  }
  onChange(e, index, value) {
    const { dispatch } = this.props;
    // Check to see if we're editing an existing subject
    if (!this.props.new) {
      // Changing the input fields should update the state of the active subject
      const sub = this.props.subject;
      sub.organization = e.value;
      dispatch(SubjectActions.setActiveSubject(sub));
    } else {
      const newSub = this.props.newSubject;
      newSub.organization = e.value;
      this.props.orgs.forEach((org) => {
        if (value == org.id) {
          newSub.organization_id_label = org.subject_id_label
        }
      })
      this.setState({value: e});
      dispatch(SubjectActions.setNewSubject(newSub));
    }
  }

  render() {
    const orgs = this.props.orgs;
    let errorText = '';

    if (this.props.error) {
      errorText = 'Please select an organization.';
    }
    return (
      <div>
        <h6 className="category"> Organization </h6>
          <Select
            onChange={this.onChange}
            value={this.props.value}
            options={this.orgOptions()}
            placeholder="Search for Organization"
          />
      </div>
    );
  }
}

SubjectOrgSelectField.propTypes = {
  dispatch: PropTypes.func,
  new: PropTypes.bool,
  orgs: PropTypes.array,
  subject: PropTypes.object,
  newSubject: PropTypes.object,
  error: PropTypes.string,
  value: PropTypes.number,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    newSubject: state.subject.newSubject,
    orgs: state.protocol.orgs,
    value: state.value,
  };
}

export default connect(mapStateToProps)(SubjectOrgSelectField);
