import { ko } from 'libs/knockout-3.4.0.js';
import { $, $$ } from 'libs/bliss.js';

var model = {
    id: ko.observable(''),
    idValid: ko.pureComputed(() => /^[A-Za-z0-9_\-]+$/.test(model.id())),

    searching: ko.observable(false),

    FindWhiteboard: function() {
        if(!model.idValid())
            return;

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
    },

    confirmCreate: ko.observable(false),

    CreateBoard: function() {
        location.assign('/board/create/' + model.id());
    }
};

model.id.subscribe(function() {
    model.confirmCreate(false);
});

$.ready(function() {
    ko.applyBindings(model, document.getElementById('main'));
});
