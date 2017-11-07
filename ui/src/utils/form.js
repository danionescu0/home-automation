import React, {Component} from 'react';

const withForm = WrapperComponent => class extends Component {
    constructor(props) {
        super(props);
        this.state = {
            form: {}
        }
    }

    handleInputChange(event) {
        const target = event.target;
        const name = target.name;

        let value = target.value;
        if (target.type === 'checkbox') {
            value = target.checked;
        } else  if(target.type === 'select-multiple') {
            value = this.getSelectedValue(target);
        }

        this.setState(function(prevState, props) {
            let form = prevState.form;
            form[name] = value;

            return {form: form};
        });
    }

    getSelectedValue(target) {
        const selectedValues = [];
        Object.values(target.options).forEach(option => option.selected ? selectedValues.push(option.value) : null);

        return selectedValues;
    }

    render() {
        return (
            <WrapperComponent {...this.props} form={this.state.form} handleInputChange={this.handleInputChange.bind(this)}/>
        )
    }
};


export default withForm;