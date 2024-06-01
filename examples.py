
app.add_url_rule('/cover','cover',build_static_page('cover.html'))
app.add_url_rule('/yearly_goals','yearly_goals',build_goals('Annual Goals','','',yearly['goals']))
app.add_url_rule('/themes','themes',build_icon_list('Themes',4,'rainbow.png'))
app.add_url_rule('/body_fat','body_fat',build_body_fat('2024'))
app.add_url_rule('/new_games','new_games',build_icon_list('New Video Games',12,'joystick.png'))
app.add_url_rule('/books','books',build_icon_list('Books (P=Paper, A=Audiobook)',25,'book.png'))
app.add_url_rule('/notable_events','notable_events',build_icon_list('Notable Events',12,'calendar.jpg'))
app.add_url_rule('/pixels','pixels',build_pixels())
app.add_url_rule('/community_events','community_events',build_icon_list('Community Events',12,'calendar.jpg'))
app.add_url_rule('/camping_trips','camping_trips',build_icon_list('Camping Trips',6,'tent.png'))
app.add_url_rule('/gigi_time','gigi_time',build_picture_grid('Gigi Time','grandma.webp',4,3))
app.add_url_rule('/call_nathan','call_nathan',build_picture_grid('Call Nathan','phone.jpg',4,3))
app.add_url_rule('/call_brady','call_brady',build_picture_grid('Call Brady','phone.jpg',4,3))
app.add_url_rule('/date_night','date_night',build_picture_grid('Date Night','hearts.gif',4,3))



app.add_url_rule('/sour_dough','sour_dough',
                 build_sectional_icon_list('Sour Dough Experiments', [f'Try {i+1}' for i in range(4)],4,'notebook.png'))

app.add_url_rule('/health_cookie','health_cookie',
                 build_sectional_icon_list('Health Cookie Experiments', [f'Try {i+1}' for i in range(6)],2,'notebook.png'))

columns = [('','10'),('Lesson',90)]
rows = [('<img src="http://localhost:5000/static/vegetable academy.png" style="height: 25px;"/>',i) for i in [
    '1.1: Grower Assessment',
    '1.2: Site Assessment',
    '1.3: Getting In the Zone',
    '2.1: Bed Layout',
    '2.2: Calculating Production',
    '2.3: Garden Planning',
    '2.4: Seed Selection',
    '3.1: Soil Preparation',
    '3.2: Irrigation Systems',
    '3.3: Weed Management',
    '3.4: Supporting Infrastructure',
    '4.1: Your Planting Log',
    '4.2: Indoor Planting Techniques',
    '4.3: Outdoor Planting Techniques',
    '5.1: Pruning',
    '5.2: Trellising',
    '5.3: Pest Management',
    '5.4: Season Extension',
    '6.1: Harvest Timing',
    '6.2: Harvest Handling',
    '6.3: Curing Storage Crops',
    '7.1: Storage Zones',
    '7.2: Processing Methods',
    '8.1: Eating in Season',
    '8.2: Waste Management'
]]

app.add_url_rule('/seed_to_table','seed_to_table',build_table('Seed to Table',columns,rows))

app.add_url_rule('/family_game_night','family_game_night',
                 build_weekly(dates, 'Family Game Night!',Day_Of_Week.SUNDAY,'pegs and a die.jpg'))