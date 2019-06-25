import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import red from '@material-ui/core/colors/red';
import Icon from '@material-ui/core/Icon';
import AddIcon from '@material-ui/icons/Add';
import Fab from '@material-ui/core/Fab';

const styles = theme => ({
  root: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'flex-end',
  },
  icon: {
    marginLeft: '10px',
    marginTop: '10px',
    float: 'right',
    backgroundColor: '#fdedf1',
    color: '#34BFED',
  },
  iconHover: {
    margin: theme.spacing.unit * 2,
    '&:hover': {
      color: red[800],
    },
    float: 'right',
  },
});

// const addButtonStyle = {
//   marginLeft: '10px',
//   marginTop: '10px',
//   float: 'right',
// };


function AddButton(props) {
  const { classes } = props;

  return (

    <Fab aria-label="Add" size="small" className={classes.icon}>
        <AddIcon />
      </Fab>
  );
}

AddButton.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AddButton);
