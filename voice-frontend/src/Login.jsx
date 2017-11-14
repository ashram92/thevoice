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
        event.preventDefault();
        this.props.handleSubmit(event, this.state.username, this.state.password);
    }

    render() {
        return (
            <form>
                <h1 className='login-form-title'>Login</h1>
                <div className='form-group'>
                    <label>Username</label>
                    <input
                        className='form-control'
                        value={this.state.username}

                        onChange= {(event) =>
                            this.setState({username:event.target.value})
                        }

                        type="text"
                    />
                </div>
                <div className='form-group'>
                    <label>Password</label>
                    <input
                        className='form-control'
                        value={this.state.password}

                        onChange= {(event) =>
                            this.setState({password:event.target.value})
                        }

                        type="password"
                    />
                </div>

                <button className='btn btn-primary btn-block'
                        onClick={this.handleSubmit}
                        onSubmit={this.handleSubmit}>Submit</button>
            </form>
        );
    }
}

export default Login;
