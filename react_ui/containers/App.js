import React from 'react';
import PropTypes from 'prop-types';
import NotificationSystem from 'react-notification-system';
import Navbar from '../components/Navbar';
import { connect } from 'react-redux';
import * as ProtocolActions from '../actions/protocol';
import * as NotificationActions from '../actions/notification';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.notificationSystem = null;
  }

  componentDidMount() {
    const { dispatch } = this.props;
    this.notificationSystem = this.refs.notificationSystem;
    if (!this.props.params.prot_id || !this.props.protocol.isFetching) {
      dispatch(ProtocolActions.fetchProtocols());
    }
  }

  componentWillReceiveProps() {
    this.processNotifications();
  }

  processNotifications() {
    // First check that the notification system is available
    const { dispatch } = this.props;
    if (this.notificationSystem) {
      // Always reset the notification systems state we are managing it through redux
      this.notificationSystem.state.notifications = [];

      // Iterate over the notifications in your state
      this.props.notifications.items.forEach((notification) => {
        // Define callback to remove notification when done display
        /* eslint-disable no-param-reassign*/
        notification.onRemove = (n) => {
          dispatch(NotificationActions.removeNotification(n));
        };
        /* eslint-enable no-param-reassign*/
        // Add notification to system state
        this.notificationSystem.addNotification(notification);
      }, this);
    }
  }

  render() {
    const style = {
      NotificationItem: { // Override the notification item
        DefaultStyle: { // Applied to every notification, regardless of the notification level
          margin: '52px 0px 2px 1px',
        },
      },
    };
    return (
      <div>
        <Navbar activeProtocolId={this.props.protocol.activeProtocolId} />
        <NotificationSystem style={style} ref="notificationSystem" />
        {this.props.children}
      </div>
    );
  }
}

App.propTypes = {
  dispatch: PropTypes.func,
  protocol: PropTypes.object,
  notifications: PropTypes.object,
  params: PropTypes.object,
  children: PropTypes.object,
};

function mapStateToProps(state) {
  return {
    protocol: {
      items: state.protocol.items,
      activeProtocolId: state.protocol.activeProtocolId,
      isFetching: state.protocol.isFetching,
    },
    notifications: {
      items: state.notification.items,
    },
  };
}

export default connect(mapStateToProps)(App);
