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
const TEAMS_URL = BASE_URL + '/candidates/api/teams/'


class Team extends Component {
    constructor(props) {
        super(props);
        this.state = {
            teamID: props.teamID,
            name: props.name,
            mentor: props.mentor,
            averageScore: props.averageScore,
            candidates: props.candidates

        };
    }

    render() {
        return (
            <div>
                <h3>{this.state.name} [Avg: {Math.round(this.state.averageScore)}] (Mentor: {this.state.mentor})</h3>
                <ul>
                    {this.state.candidates.map(function(candidate, i) {
                        return (<li key={candidate.id}><b>{candidate.name}</b> [Avg: {Math.round(candidate.average_score)}]
                            <ul>
                                {candidate.activities.map(function(activity, j){
                                   return (<li key={activity.id}>{activity.song_name} | Date: {activity.performance_date} | Avg Score: {Math.round(activity.average_score)}</li>);
                                })}
                            </ul>
                        </li>);
                    })}
                </ul>
            </div>
        )
    }

}


class Profile extends Component {
    constructor(props) {
        super(props);
        this.state = {
            profile: null,
            teams: null,
            displayedTeams: []
        };
    }

    filterList = (event) => {
        var filteredTeams = this.state.teams;
        filteredTeams = filteredTeams.filter(function(team){
            return team.name.toLowerCase().search(
                event.target.value.toLowerCase()) !== -1;
        });
        this.setState(state => ({...state, displayedTeams: filteredTeams}));
    }

    componentDidMount() {
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
            return axios.get(TEAMS_URL);

        }).then((response) => {
            this.setState(state => ({
                profile: state.profile,
                teams: response.data,
                displayedTeams: response.data
            }));
            return;
        }).catch(error => {
           if (error.status === 403) {
               alert('You are not logged in');
               this.props.invalidateSession();
           } else {
               alert('Error occured! Please refresh the page');
           }
        });
    }

    render() {
        const { profile, teams, displayedTeams } = this.state;
        if (profile === null || teams === null) { // TODO: Is there a better way of doing this?
            return (<div>Loading...</div>)
        }

        var teamsDiv;

        if (teams.length == 0) {
            teamsDiv = (<div>
                <h3>You have no teams to view!</h3>

            </div>);
        } else {
            teamsDiv = (<div>
                <h1>Teams</h1>
                {profile.isAdmin === true &&
                    <div>
                        <label>Filter by team name: </label>
                        <input onChange={this.filterList} type="text" />
                    </div>
                }
                {displayedTeams.map(function(team, i){
                    return <Team key={team.id} teamID={team.id} name={team.name} mentor={team.mentor} candidates={team.candidates} averageScore={team.average_score}/>
                })};
            </div>);
        }



        return (
            <div>
                <div>
                    Logged in as: {profile.username}
                    <button className="logout-button" onClick={this.props.handleLogout}>Logout</button>
                </div>
                {teamsDiv}
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
      if (this.state.isLoggedIn) {
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
