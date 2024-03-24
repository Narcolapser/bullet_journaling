@app.route('/disc')
def disc():
    date1 = datetime.strptime('2021-04-06', '%Y-%m-%d')
    date2 = datetime.strptime('2021-04-09', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        dates.append(date2)
        date1 = date1 + week_delta
        date2 = date2 + week_delta
    return render_template('disc.html',dates=dates)

@app.route('/bitcoin')
def bitcoin():
    rows = 4
    cols = 3
    title = "Bitcoin for the Befuddled"
    picture = 'bitcoin.png'
    return render_template('picture_grid.html',rows=4, cols=3, title=title, picture=picture)

@app.route('/running')
def running():
    date1 = datetime.strptime('2021-04-05', '%Y-%m-%d')
    date2 = datetime.strptime('2021-04-07', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        dates.append(date2)
        date1 = date1 + week_delta
        date2 = date2 + week_delta
    units = ['Heart Rate (BPM)','Distance (M)','Time (m)']
    unit_steps = [range(100,180,4),[v/10.0 for v in range(10,30)],range(10,30)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

@app.route('/crypto_investing')
def crypto_investing():
    return render_template('large_item_table.html',rows=6,title='Crypto Investing',
                           top_prompt='Reason',bottom_prompt='Initial Investment')
                           
@app.route('/board_games')
def board_games():
    return render_template('icon_list.html',title='New Board/Card Games',rows=12,img='d20.png',height='50')

@app.route('/camping')
def camping():
    return render_template('icon_list.html',title='Camping',rows=6,img='tent.png',height='100')

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

@app.route('/body_fat')
def body_fat():
    months = ['April','May','June','July','August','September','October','November','December',
              'January','February','March']
    return render_template('body_fat.html',months=months)

@app.route('/cover')
def cover():
    return render_template('cover.html')

@app.route('/yearly_goals')
def yearly_goals():
    title = '2021 Goals'
    goals = ['Learn to plumb','Draw 80 times','Brew a Rootbeer with a Gingerbug','Play 12 new video games','play 12 new board/card games','Read all of Harry Potter','Daily language lessons','Develop a six pack','Monthly Call w/ brady','Monthly Gigi time','Monthly tarts','Quarterly guys night','Do some freelance devops/dev work','Invest in stocks and crypto','Finish "Queens Theif" series','Read "Bitcoin for the Befuddled"','Setup Bible memorization scheme','Memorize several chunks of the Bible','Read a theology book','Beat ringfit','Track body fat','Run twice a week in summer','Teach Lucy "swim"','Make Lucy a mud kitchen','Get Lucy\'s car working','Migrate off of gmail to ProtonMail']
    return render_template('goals.html',title=title,goals=goals)

@app.route('/spring_goals')
def spring_goals():
    title = 'Spring 2021'
    subtitle = 'Season of Enjoying'
    goals = ['Brew a root beer with ginger bug','Play 3 new video games (min 3 hours)','Have a guys night','Read "Bitcoin for the Befuddled"','Invest in some Cryptos','Design Bible Memorization scheme','Fix Lucy\'s car','Invite someone over','Beat Prentis in 30 throws','Draw twice a week']
    return render_template('goals.html',title=title,goals=goals,subtitle=subtitle)

@app.route('/arms')
def arms():
    dates = get_date_sequence(FRIDAY)
    items = ['Chest Press','Angel','Bicep Curl','Tricep Curl','Bent Over Row']
    steps = 5
    item_bounds = [[40,90],[24,75],[20,60],[20,60],[20,60]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Weight Lifting: Arms',items=items,
        item_units=item_units, steps=steps)