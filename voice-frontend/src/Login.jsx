import React from 'react';

class Login extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        };
    }

    handleSubmit = (event) => {
        this.props.handleSubmit(event, this.state.username, this.state.password);
    }

    render() {
        return (
            <div className='login-form-container'>
                <div className='login-form'>
                    <h2>Login:</h2>
                    <div>
                        <label>Username: </label>
                        <input
                            value={this.state.username}

                            onChange= {(event) =>
                                this.setState({username:event.target.value})
                            }

                            type="text"
                        />
                    </div>
                    <div>
                        <label>Password: </label>
                        <input
                            value={this.state.password}

                            onChange= {(event) =>
                                this.setState({password:event.target.value})
                            }

                            type="password"
                        />
                    </div>
                    <button className='login-button'
                            onClick={this.handleSubmit}>Submit</button>
                </div>
            </div>
        );
    }
}

export default Login;
