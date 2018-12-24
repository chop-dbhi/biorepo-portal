import React from 'react';
import { connect } from 'react-redux';
import SelectField from 'material-ui/lib/select-field';
import MenuItem from 'material-ui/lib/menus/menu-item';
import * as SubjectActions from '../../../actions/subject';

class SubjectOrgSelectField extends React.Component {
  constructor(props) {
    super(props);
    this.onChange = this.onChange.bind(this);
  }

  onChange(e, index, value) {
    const { dispatch } = this.props;
    // Check to see if we're editing an existing subject
    if (!this.props.new) {
      // Changing the input fields should update the state of the active subject
      const sub = this.props.subject;
      sub.organization = value;
      dispatch(SubjectActions.setActiveSubject(sub));
    } else {
      const newSub = this.props.newSubject;
      newSub.organization = value;
      this.props.orgs.forEach((org) => {
        if (value == org.id) {
          newSub.organization_id_label = org.subject_id_label
        }
      })
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
      <SelectField
        onChange={this.onChange}
        style={{ width: '100%', whiteSpace: 'nowrap' }}
        value={this.props.value}
        errorText={errorText}
        floatingLabelText={'Organization'}
      >
        {orgs ?
          orgs.map((org, i) => (
            <MenuItem key={i} value={org.id} primaryText={org.name} />
          )) : <MenuItem />}
      </SelectField>
    );
  }
}

SubjectOrgSelectField.propTypes = {
  dispatch: React.PropTypes.func,
  new: React.PropTypes.bool,
  orgs: React.PropTypes.array,
  subject: React.PropTypes.object,
  newSubject: React.PropTypes.object,
  error: React.PropTypes.string,
  value: React.PropTypes.number,
};

function mapStateToProps(state) {
  return {
    subject: state.subject.activeSubject,
    newSubject: state.subject.newSubject,
    orgs: state.protocol.orgs,
  };
}

export default connect(mapStateToProps)(SubjectOrgSelectField);
