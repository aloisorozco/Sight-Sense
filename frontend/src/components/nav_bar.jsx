import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import classes from './nav_bar.module.css';

function NavBar() {
    return (
        <nav className={`navbar navbar-expand-lg navbar-dark bg-dark shadow ${classes.nav}`}>
            <div className={`container-fluid ${classes.container}`}>
                <div className="navbar-brand">
                    <h1>👓</h1>
                </div>
                <div>
                    <a className={`nav-link ${classes.link}`}>About</a>
                </div>
            </div>
        </nav>
    );
}

export default NavBar;
