<script type="text/javascript">
$(document).ready(function() {
    var baseURL = '{{ request.HTTP_X_FORWARDED_HOST }}/read/';
    var staticURL = '{{ STATIC_URL }}/media/';
    var theURL = '';

    var bookSlug = {% if pages.book %}'{{ pages.book.slug }}'; {% else %}'';{% endif %}
    var chapterSlug = {% if pages.chapter %}'{{ pages.chapter.slug }}'{% else %}'';{% endif %}
    var pageNumber = {% if pages.currentPage %}{{ pages.currentPage.pnumber }}{% else %}1{% endif %};

    var nextNum{% if pages.nextPage %} = {{ pages.nextPage.pnumber }}{% endif %};
    var prevNum{% if pages.previousPage %} = {{ pages.previousPage.pnumber }}{% endif %};    
    var theURL = '';

    var pagecount = {{ pages.chapter.page_set.count }};   
    
    function buildURL() {
        theURL = baseURL.concat(bookSlug,'/',chapterSlug,'/',pageNumber);
        return theURL;
    }

    function getPages() {
        $.getJSON(buildURL(), function(data){
                $('.page-nav-current').removeClass("page-nav-current");
                artURL = data.currentPage.fields.art;
                pageNumber = data.currentPage.fields.pnumber;

                if(data.nextPage==0){
                    $('#controls-next').animate({width: '0%',});
                } else {
                    $('#prefetch-next').attr('src', staticURL+data.nextPage.fields.art)
                    nextNum = data.nextPage.fields.pnumber;               
                    $('#controls-next').animate({width: '50px',});
                }

                if(data.previousPage==0){
                    $('#controls-previous').animate({width: '0%',});
                } else { 
                    $('#prefetch-prev').attr('src', staticURL+data.previousPage.fields.art)
                    prevNum = data.previousPage.fields.pnumber;
                    $('#controls-previous').animate({width: '50px',});
                }

//                var output = require( "markdown" ).toHTML( data.currentPage.fields.text );
//                alert(output);

                $('#current-image').attr('src', staticURL+artURL);
                $('#current-image').attr('alt', data.currentPage.fields.published);
                $('#page-nav-'+pageNumber).addClass('page-nav-current');
                $('#fb-like').attr('href', theURL);
                $('#twitter-button').attr('data-url', theURL);
                return 1;
        });
    }

    for(var i=1; i<={{ pages.chapter.page_set.count }}; i++) {
        if(i==pageNumber) {
            $('<li id="page-nav-'+i+'" class="page-nav-list page-nav-current">'+i+'</li>').appendTo('#page-nav');
        } else {
            $('<li id="page-nav-'+i+'" class="page-nav-list">'+i+'</li>').appendTo('#page-nav');
        }
    }

    getPages();


    $('#controls-next').click(function() {
        $('#controls-next').attr('src',"{{ STATIC_URL }}img/loading-spiral.gif");
        $('#comic-page').animate({
                opacity: 0, 
                width: '0%'
            },1000, function() {
                pageNumber = nextNum
                getPages();        
                $('#current-image').load(function() {
                    $('#comic-page').animate({opacity:100, width: '100%'}, 1000, function(){});
                    $('#controls-next').attr('src',"{{ STATIC_URL }}img/next-arrow.gif");
                });
            });
    });


    $('#controls-previous').click(function() {
        $('#controls-previous').attr('src',"{{ STATIC_URL }}img/loading-spiral.gif");
        $('#comic-page').animate({
                opacity: 0,
                width: '0%'
            },1000, function() {
                pageNumber = prevNum
                getPages();
                $('#current-image').load(function() {
                    $('#comic-page').animate({opacity:100, width: '100%'}, 1000, function(){});
                    $('#controls-previous').attr('src',"{{ STATIC_URL }}img/back-arrow.gif");
            });    
        });
    });

});

</script>
