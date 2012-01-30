{% load markup %}
<script type="text/javascript">
$(document).ready(function() {
    var mediaURL = '{{ MEDIA_URL }}/';
    var theURL = '';
    var pageCount = {{ pages.count }};

    function disqusReset(identifier, url) {
       DISQUS.reset({
              reload: true,
              config: function () {
                        this.page.identifier = identifier;
                        this.page.url = 'http://rigbythebarbarian.com'+url;
                    }
              });
    }

    function page(pk, URL, author, artist, colorist, pnumber, published, artURL, text) {
        self.pk = pk;
        self.URL = URL;
        self.author= author;
        self.artist = artist;
        self.colorist = colorist;
        self.pnumber = pnumber;
        self.published = published;
        self.artURL = artURL;
        self.text = text;
    }

    function bts(URL, title, text) {
        self.URL = URL;
        self.title = title;
        self.text = text;
    }

    pages = new Array(pageCount-1); {% for page in pages %}
        pages[{{ forloop.counter0}}] = new page();
        pages[{{ forloop.counter0}}].id = {{ page.id }};
        pages[{{ forloop.counter0}}].title = '{{ page.title }}';
        pages[{{ forloop.counter0}}].URL = '{{ page.get_absolute_url }}';
        pages[{{ forloop.counter0}}].author = '{% for author in page.author.get_query_set %}{{ author }}{% if not forloop.last %}, {% endif %}{% endfor %}';
        pages[{{ forloop.counter0}}].artist = '{% for artist in page.artist.get_query_set %}{{ artist }}{% if not forloop.last %}, {% endif %}{% endfor %}';
        pages[{{ forloop.counter0}}].colorist = '{% for colorist in page.colorist.get_query_set %}{{ colorist }}{% if not forloop.last %}, {% endif %}{% endfor %}';
        pages[{{ forloop.counter0}}].pnumber = '{{ page.pnumber }}'
        pages[{{ forloop.counter0}}].published = '{{ page.published }}';
        pages[{{ forloop.counter0}}].artURL = '{{ page.art.url }}';
        pages[{{ forloop.counter0}}].text = "<h3>{{ page.published }}</h3>{% spaceless %}{{ page.text|markdown|addslashes }}{% endspaceless %}"; 
        {% if page.bts_set.count %}pages[{{ forloop.counter0}}].bts = new Array({{ page.bts_set.count }});{% for bts in page.bts_set.all %}
            bts[{{ forloop.counter0}}] = new bts();
            bts[{{ forloop.counter0}}].URL = '{{ bts.art.url }}';
            bts[{{ forloop.counter0}}].title = '{{ bts.title }}';
            bts[{{ forloop.counter0}}].text = "{% spaceless %}{{ bts.text|markdown|addslashes }}{% endspaceless %}";
        {% endfor %}{% else %}pages[{{ forloop.counter0}}].bts = null;{% endif %}
    {% endfor %}

    if(window.location.hash) {
        var theHash = window.location.hash;
        theHash = theHash.match(/(\D\D)(\d{1,2})/);
        theHash = eval(theHash[2]); 
        var currentIndex = theHash-1;
        if(theHash>1) {
            setCurrent();
        }
    } else {
        var currentIndex = 0;
        window.location.hash = '!1';
    }
    
    var disqus_shortname = 'rigbythebarbarian'; // required: replace example with your forum shortname
    var disqus_identifier = pages[currentIndex].id;
    var disqus_url = 'http://rigbythebarbarian.com'+pages[currentIndex].url;

    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);


    function setCurrent() {
        currentPage = pages[currentIndex];

        $('#comic-page').animate({
                opacity: 0,
                width: '0%'
            },1000, function() {
                $('#current-image').attr('src', currentPage.artURL); 
                $('#page-text').empty().append(currentPage.text);            
                $('.page-nav-current').removeClass('page-nav-current');
                $('#page-nav-'+currentPage.pnumber).addClass('page-nav-current');
                $('#chapter-page-label').empty().append(currentPage.pnumber);


                $('#fb-like').attr('href', currentPage.URL);


                $('#twitter-button').find('a.twitter-share-button').each(function(){
                    var tweet_button = new twttr.TweetButton( $( this ).get( 0 ) );
                    tweet_button.render();
                });



                $('#artist-name').html(currentPage.artist);
                $('#author-name').html(currentPage.author);        
                $('#colorist-name').html(currentPage.colorist);        



                $('#comic-page').animate({
                        opacity: 100,
                        width: "100%"
                    }, 1000, function() {});

                if(currentIndex > 0) {
                    previousPage = pages[currentIndex-1];
                    $('#controls-prev').animate({width: '40px',});
                    $('#prefetch-prev').attr('src', previousPage.artURL)
                } else  {
                    $('#controls-prev').animate({width: '0%',});
                }

                if(currentIndex < pageCount) {
                    if( currentIndex != pageCount-1) {
                        $('#controls-next').animate({width: '40px',});
                        nextPage = pages[currentIndex+1];
                    } else {
                        $('#controls-next').animate({width: '0%',});
                        nextPage = currentPage;
                    }

                    $('#prefetch-next').attr('src', nextPage.artURL)
                } else {
                    $('#controls-next').animate({width: '0%',});
                }

                $.getJSON('http://rigbythebarbarian.com/session/remember/'+currentPage.id+'/', function(data){
                //$.getJSON('http://test.apt9online.com/session/remember/'+currentPage.id+'/', function(data){
                });
                    
        });

        
    }

    //Some page initializations
    if(currentIndex==0) {
        $('#controls-prev').animate({width: '0%',});
    }
    if(currentIndex==pageCount-1) {
        $('#controls-next').animate({width: '0%',});
    }

    $('#artist-name').html(pages[currentIndex].artist);        
    $('#author-name').html(pages[currentIndex].author);        
    $('#colorist-name').html(pages[currentIndex].colorist);        
    $('#page-text').prepend('<h3>'+pages[currentIndex].published+'</h3>');

    //Build the li list for pages
    for(var i=0; i<pageCount; i++) {
        if(i==currentIndex) {
            $('<li id="page-nav-'+(i+1)+'" class="page-nav-list page-nav-current"><a class="page-nav-link" href="javascript:void(0)">'+(i+1)+'</a></li>').appendTo('#page-nav');
        } else {
            $('<li id="page-nav-'+(i+1)+'" class="page-nav-list"><a class="page-nav-link" href="javascript:void(0)">'+(i+1)+'</a></li>').appendTo('#page-nav');
        }
    }

    $('#controls-next').click(function() {
        $('#controls-next').attr('src',"{{ STATIC_URL }}/img/loading-spiral.gif");
        currentIndex += 1;
        window.location.hash = '!'+(currentIndex+1);
         $.when(setCurrent()).done(function () {
            $('#controls-next').attr('src',"{{ STATIC_URL }}/img/next-arrow.gif");
        });

    });


    $('#controls-prev').click(function() {
        $('#controls-prev').attr('src',"{{ STATIC_URL }}/img/loading-spiral.gif");
        currentIndex -= 1; 
        window.location.hash = '!'+(currentIndex+1);
        $.when(setCurrent()).done(function () {
            $('#controls-prev').attr('src',"{{ STATIC_URL }}/img/back-arrow.gif");
        });
    });

    $('.page-nav-link').click(function() {
        currentIndex = eval($(this).html())-1;
        window.location.hash = '!'+(currentIndex+1); 
        setCurrent();
    });

    $(window).bind('hashchange', function() {
        disqusReset(pages[currentIndex].id, pages[currentIndex].URL);
    });
    

});
</script>
