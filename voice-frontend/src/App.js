import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Login from './Login';
import axios from 'axios';
import Cookies from 'universal-cookie';

const BASE_URL = ''; // 'http://127.0.0.1:8000';
const LOGIN_URL = BASE_URL + '/accounts/api/login/';
const LOGOUT_URL = BASE_URL + '/accounts/api/logout/';
const PROFILE_URL = BASE_URL + '/accounts/api/profile/';


class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            profile: null
        };
    }

    componentDidMount() {
        console.log('Hi0');
        axios.get(PROFILE_URL).then(response => {
            this.setState(state => ({
                profile: {
                    userId: response.data.id,
                    username: response.data.username,
                    firstName: response.data.first_name,
                    lastName: response.data.last_name,
                    isAdmin: response.data.is_admin,
                    isMentor: response.data.is_mentor
                }
            }));
            console.log(this.state);
        }).catch(error => {
           if (error.status === 403) {
               alert('You are not logged in');
               this.props.invalidateSession();
           }
        });
    }

    render() {
        var profile = this.state.profile;
        if (profile === null) { // TODO: Is there a better way of doing this?
            return (<div>Loading...</div>)
        }
        return (
            <div>
                <div>
                    Username: {profile.username}
                </div>
                You are logged in {profile.firstName} {profile.lastName}!
                <button onClick={this.props.handleLogout}>Logout</button>
            </div>
        );
    }
};


class App extends Component {
    constructor(props) {
        super(props);
        this.cookie = new Cookies();
        this.state = {
            isLoggedIn: this.checkLoggedIn()
        };
    }

    checkLoggedIn = () => {
        if (this.cookie.get('loggedIntoVoice') === '1') {
            return true;
        }
        return false;
    }

    setLoggedIn = () => {
        this.cookie.set('loggedIntoVoice', '1');
        this.setState(state => ({...state, isLoggedIn: true}));
    }

    invalidateSession = () => {
        this.cookie.remove('loggedIntoVoice');
        this.setState(state => ({...state, isLoggedIn: false}));
    }

    handleLogin = (event, username, password) => {
        axios.post(LOGIN_URL, {
            username: username,
            password: password,
        }).then(response => {
            this.setLoggedIn();
        }).catch(error => {
            this.invalidateSession();
            alert('Bad login details!');
        });
    }

    handleLogout = (event) => {
        axios.get(LOGOUT_URL).then(
            response => {
                return this.invalidateSession();
            }
        ).catch(
            error => {
                return this.invalidateSession();  // Fallback to logging out.
            }
        );
    }

  render() {
      var component;
      if (this.checkLoggedIn()) {
          component = <Profile handleLogout={this.handleLogout}
                               invalidateSession={this.invalidateSession}/>;
      } else {
          component = <Login handleSubmit={this.handleLogin}/>;
      }

      return (
          <div className="App">
              {component}
          </div>
      );
  }
}

export default App;
