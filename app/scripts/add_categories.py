print('add_categories.py script is running')
try:
    from app import create_app, db
    from app.models import Category
except Exception as e:
    print(f"Import error: {e}")
    raise

def add_categories():
    try:
        app = create_app()
        print("Script started!")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    except Exception as e:
        print(f"App creation error: {e}")
        raise
    with app.app_context():
        # Define new categories with descriptions
        categories = [
            Category(name='Sports', description='Athletic events, competitions, and tournaments'),
            Category(name='Music', description='Concerts, festivals, and musical performances'),
            Category(name='Conference', description='Business meetings, seminars, and professional gatherings'),
            Category(name='Exhibition', description='Art shows, trade fairs, and displays'),
            Category(name='Theater', description='Plays, musicals, and dramatic performances'),
            Category(name='Comedy', description='Stand-up shows, comedy nights, and humorous performances'),
            Category(name='Dance', description='Ballet, contemporary dance, and dance competitions'),
            Category(name='Food & Drink', description='Food festivals, wine tastings, and culinary events'),
            Category(name='Education', description='Workshops, lectures, and educational programs'),
            Category(name='Charity', description='Fundraising events, galas, and community gatherings'),
            Category(name='Technology', description='Tech conferences, hackathons, and innovation events'),
            Category(name='Fashion', description='Fashion shows, launches, and industry events'),
            Category(name='Gaming', description='Gaming tournaments, conventions, and esports events'),
            Category(name='Film', description='Movie premieres, film festivals, and screenings'),
            Category(name='Literature', description='Book launches, poetry readings, and literary festivals'),
            Category(name='Health & Wellness', description='Yoga, meditation, and wellness retreats'),
            Category(name='Kids & Family', description='Family-friendly and children\'s events'),
            Category(name='Networking', description='Meetups, mixers, and professional networking'),
            Category(name='Religious', description='Religious gatherings, festivals, and ceremonies'),
            Category(name='Outdoor', description='Hiking, camping, and outdoor adventures'),
            Category(name='Science', description='Science fairs, lectures, and STEM events'),
            Category(name='Motorsport', description='Car shows, races, and motorsport events'),
            Category(name='Pets & Animals', description='Pet shows, adoption events, and animal expos'),
            Category(name='Home & Garden', description='Home improvement, gardening, and decor events'),
            Category(name='Travel', description='Travel expos, tourism fairs, and adventure events'),
            Category(name='Business', description='Business expos, entrepreneurship, and trade shows'),
            Category(name='Startup', description='Startup pitches, demo days, and incubator events'),
            Category(name='Photography', description='Photo walks, exhibitions, and workshops'),
            Category(name='Crafts', description='DIY, crafting, and maker events'),
            Category(name='Cultural', description='Cultural festivals, heritage, and traditions'),
            Category(name='Politics', description='Political rallies, debates, and forums'),
            Category(name='Environment', description='Eco-friendly, sustainability, and green events'),
            Category(name='Magic', description='Magic shows and illusionist performances'),
            Category(name='Martial Arts', description='Martial arts tournaments and exhibitions'),
            Category(name='Auction', description='Charity and public auctions'),
            Category(name='Other', description='Miscellaneous events')
        ]

        # Add categories to database
        for category in categories:
            # Check if category already exists
            existing = Category.query.filter_by(name=category.name).first()
            if not existing:
                db.session.add(category)
                print(f"Added category: {category.name}")
            else:
                print(f"Category already exists: {category.name}")

        try:
            db.session.commit()
            print("\nCategories added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"\nError adding categories: {str(e)}")

        # Print all categories in the database
        print("\nCurrent categories in the database:")
        all_categories = Category.query.all()
        for cat in all_categories:
            print(f"- {cat.id}: {cat.name} ({cat.description})")

if __name__ == '__main__':
    add_categories() 