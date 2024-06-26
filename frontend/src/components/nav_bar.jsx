import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import classes from './nav_bar.module.css';

function NavBar() {
    return (
        <nav className={`navbar navbar-expand-lg navbar-dark bg-dark shadow fixed-top" ${classes.nav}`}>
            <div className={`container-fluid ${classes.container}`}>
                <div className="navbar-brand">
                    <h1>👓</h1>
                </div>
                <div>
                    <button type="button" className={`btn btn-light ${classes.link}`}>Log-In</button>
                </div>
            </div>
        </nav>
    );
}

export default NavBar;
