//import * from './libs/knockout-3.4.0.js';
//import * from './libs/bliss.js';

var model = {
    id: ko.observable(''),
    idValid: ko.pureComputed(() => /^[A-Za-z0-9_\-]+$/.test(model.id())),

    searching: ko.observable(false),

    FindWhiteboard: function() {
        if(!model.idValid())
            return false;

        var id = model.id();

        $.fetch('/exists', {
            method: 'GET',
            data: "id=" + encodeURIComponent(id) // shouldn't do anything, but just in case
        }).then(function(xhr) {
            location.assign('/board/' + encodeURIComponent(id));
        }).catch(function(error) {
            if(error.status === 404)
                model.confirmCreate(true);
            else
                alert("There was an issue connecting to the server.");
        });

        return false;
    },

    confirmCreate: ko.observable(false)
};

model.id.subscribe(function() {
    model.confirmCreate(false);
});

$.ready().then(function() {
    console.log('applying bindings')
    ko.applyBindings(model, $('#main'));
});
