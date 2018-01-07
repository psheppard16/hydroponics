$(function (){
var createList = function(selector){

    var ul = $('<ul>');
    var selected = $(selector);

    if (selected.length === 0){
        return;
    }

    selected.clone().each(function (i,e){

        var p = $(e).children('.descclassname');
        var n = $(e).children('.descname');
        var l = $(e).children('.headerlink');

        var a = $('<a>');
        a.attr('href',l.attr('href')).attr('title', 'Link to this definition');

        //a.append(p).append(n);
        n.addClass('navbar-descname');
        a.append(n);

        var entry = $('<li>').append(a);
        ul.append(entry);
    });
    return ul;
}


var c = $('<div style="float:left; min-width: 300px;">');

var ul0 = c.clone().append($('.submodule-index'))

customIndex = $('.localtoc');
customIndex.empty();
customIndex.append(ul0);

var x = [];
x.push(['Classes','dl.class > dt']);
x.push(['Methods','dl.method > dt']);
x.push(['Functions','dl.function > dt']);
x.push(['Variables','dl.data > dt']);
//x.push(['Exceptions','dl.exception > dt']);

x.forEach(function (e){
    var l = createList(e[1]);
    if (l) {        
        var ul = c.clone()
            .append('<span class="rubric" style="margin-left: 5px;">'+e[0]+'</span>')
            .append(l);
    }
    customIndex.append(ul);
});

});