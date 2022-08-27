/*global location: false, window: false, jQuery: false */
(function ($, training_votablebehavior) {
    "use strict";
    training_votablebehavior.init_voting_viewlet = function (context) {
        var notyetvoted = context.find("#notyetvoted"),
            alreadyvoted = context.find("#alreadyvoted"),
            delete_votings = context.find("#delete_votings"),
            delete_votings_confirmation = context.find("#delete_votings_confirmation");
        if (context.find("#voted").length !== 0) {
            alreadyvoted.show();
        } else {
            notyetvoted.show();
        }

        function vote(rating) {
            return function inner_vote() {
                $.post(context.find("#context_url").attr('href') + '/vote', {
                    rating: rating
                }, function () {
                    location.reload();
                });
            };
        }

        context.find("#voting_plus").click(vote(1));
        context.find("#voting_neutral").click(vote(0));
        context.find("#voting_negative").click(vote(-1));

        delete_votings.click(function () {
            delete_votings_confirmation.toggle();
        });
        delete_votings_confirmation.click(function () {
            $.post(context.find("#context_url").attr("href") + "/clearvotes", function () {
                location.reload();
            });
        });
    };
}(jQuery, window.training_votablebehavior = window.training_votablebehavior || {}));