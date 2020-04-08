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

  setOrgDefaltValue(){
    let defaultValue = null;
    defaultValue = {
      value: this.props.value,
      label: this.props.label,
    };
    return defaultValue
  }
  onChange(e, index, value) {
    const { dispatch } = this.props;
    // Check to see if we're editing an existing subject
    if (!this.props.new) {
      // Changing the input fields should update the state of the active subject
      const sub = this.props.subject;
      sub.organization = e.value;
      sub.organization_name = e.label
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
    const errorStyle = {
      control: styles => ({ ...styles, backgroundColor: '#F04D77' })
    }
    return (
      <div>
        <h5 className="category" style={{fontWeight: "bold"}}> Organization </h5>
        {this.props.editSubjectMode ?
          <Select
            onChange={this.onChange}
            defaultValue={this.setOrgDefaltValue()}
            options={this.orgOptions()}
            placeholder="Search for Organization"
            styles={this.props.error ? errorStyle : {}}
          />
          :
          <Select
            onChange={this.onChange}
            options={this.orgOptions()}
            placeholder="Search for Organization"
            styles={this.props.error ? errorStyle : {}}
          />}

        {this.props.error ? <p> {this.props.error} </p> : null  }
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
  label: PropTypes.string,
  editSubjectMode: PropTypes.bool,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    newSubject: state.subject.newSubject,
    orgs: state.protocol.orgs,
    editSubjectMode: state.subject.editSubjectMode,
  };
}

export default connect(mapStateToProps)(SubjectOrgSelectField);
