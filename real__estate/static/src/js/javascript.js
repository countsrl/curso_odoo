oddo.define('real__estate.estate.property',[
    'web.ajax',
    
], function(require) {
    'use strict';

    var ajax = require('web.ajax');

    $(document).ready(function() {
        var container = document.getElementById("property");

        if(container){
            container.innerHTML = "";
            container.innerHTML="<div  class='col text-center'> Cargando</div>";
            ajax.jsonRpc('/get_property','call',{}).then(function(data){
                container.innerHTML = "";
                console.log(data);
                for (var i=0; i<data.length; i++){
                    container.innerHTML += '<div class="col-12 col-sm-6, col-md-4 mb-3">\
                    <a href="#" class="d-block col-12 col-lg-10 text-center pt-3">\
                    <h6 class="text-center mt-3 pb-1">' +data[i].name + '</h6>\
                    </a>\
                    </div>';
                }

            });
            

        }
    })
    
});

odoo.define('real__estate.dynamic', function (require) {
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var Dynamic = PublicWidget.Widget.extend({
        selector: '.dynamic_snippet_blog',
        start: function () {
            var self = this;
            rpc.query({
                route: '/total_product_sold',
                params: {},
            }).then(function (result) {
                self.$('#total_sold').text(result);
            });
        },
    });
    PublicWidget.registry.dynamic_snippet_blog = Dynamic;
    return Dynamic;
 });