import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function Intro_Container(props) {

    return (
        <div style={{ color: '#FFFFFF',  display: 'flex', flexDirection:'column'}}>
         <span>👓 Sight Sence: AI - Powered Doorbell</span>
          <span>Project born as a way to provide a reliable, lightweight and cheap, open source alternative for people to enjoy AI powered doorbell without cashing out</span>
        </div>
    )
}

export default Intro_Container