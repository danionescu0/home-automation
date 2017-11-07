import jwt from 'jsonwebtoken';

class Auth {
    static authenticateUser(token) {
        localStorage.setItem('token', token);
    }

    static isUserAuthenticated() {
        const token = localStorage.getItem('token');
        if (token === null) {
            return false;
        }

        return Auth.isTokenValid(token);
    }

    static isTokenValid(token) {
        return jwt.decode(token).exp > Math.floor(Date.now() / 1000);
    }

    static getUserId() {
        if (!jwt.decode(Auth.getToken())) {
            return null;
        }

        return jwt.decode(Auth.getToken()).userid;
    }

    static deAuthenticateUser() {
        localStorage.removeItem('token');
    }

    static getToken() {
        return localStorage.getItem('token');
    }

}

export default Auth;