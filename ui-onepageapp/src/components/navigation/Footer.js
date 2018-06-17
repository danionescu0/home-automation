import React, {Component} from 'react';

class Footer extends Component {
  render() {
    return (
      <footer className="app-footer">
        <span><a href="https://github.com/danionescu0/home-automation">HomeAutomation &copy; documentation.</a></span>
        <span className="ml-auto">Powered by <a href="http://coreui.io">CoreUI</a></span>
        <span className="ml-auto">Icons made by <a href="http://www.freepik.com" title="Freepik">Freepik</a>
            from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by
            <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a>
        </span>
      </footer>
    )
  }
}

export default Footer;