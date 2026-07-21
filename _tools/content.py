"""All site content, kept apart from the templates in build.py.

Text and structure mirror the live Wix site (beyondthenethtx.wixsite.com/beyond-the-net),
including its typos, which are preserved deliberately so the rebuild is faithful.
"""

EMAIL = "beyondthenethtx@gmail.com"
INSTAGRAM = "https://www.instagram.com/beyondthenethtx/"

# --------------------------------------------------------------------- events
# All three are past events, which is why /events shows "No events at the moment".
EVENTS = [
    {
        "slug": "week-2-personal-statements",
        "title": "Week 2 - Personal Statements",
        "short_date": "Tue, Sep 02",
        "iso": "2025-09-02",
        "venue": "KIPP Journey Collegiate",
        "when": "Sep 02, 2025, 5:00 PM – 6:30 PM",
        "where": "KIPP Journey Collegiate, 14030 Florence Rd, Sugar Land, TX 77498",
        "status": "Registration is closed",
        "summary": "Today, we will go over the personal statement and strategies for composing a "
                   "strong, impactful narrative that will impress admission officers. We will also "
                   "be using volleyball as an example!",
        "about": "Explore college applications with sports scholarships.",
        "image": "event-week-2.jpg",
    },
    {
        "slug": "week-1-exploration",
        "title": "Week 1 - Exploration",
        "short_date": "Tue, Aug 26",
        "iso": "2025-08-26",
        "venue": "KIPP Journey Collegiate",
        "when": "Aug 26, 2025, 5:00 PM – 6:30 PM",
        "where": "KIPP Journey Collegiate, 14030 Florence Rd, Sugar Land, TX 77498",
        "status": "Registration is closed",
        "summary": "Join us for a fun-filled day designed to connect students over volleyball and "
                   "explore options for post-secondary education and the college application process!",
        "about": "Connect through sports and college readiness.",
        "image": None,
    },
    {
        "slug": "back-to-school-bash",
        "title": "Back to School Bash",
        "short_date": "Mon, Aug 04",
        "iso": "2025-08-04",
        "venue": "KIPP Journey Collegiate",
        "when": "Aug 04, 2025, 4:30 PM – 6:30 PM",
        "where": "KIPP Journey Collegiate, 14030 Florence Rd, Sugar Land, TX 77498",
        "status": "Tickets are not on sale",
        "summary": "Come meet the founders and learn more about what we do and why we do it!",
        "about": "Learn crucial leadership skills for students.",
        "image": "event-back-to-school.jpg",
    },
]

# ------------------------------------------------------------------- services
SERVICES = [
    {
        "slug": "volleyball-leadership-session",
        "title": "Volleyball Leadership Session",
        "tagline": "Elevate your volleyball skills and leadership potential.",
        "duration": None,
        "price": "$50",
        "price_long": "50 US dollars",
        "location": "Main Street",
        "cta": None,
        "unavailable": "This service is not available, please contact for more information.",
        "description": "This session focuses on developing both volleyball skills and leadership "
                       "qualities. Engage in drills and group activities designed to enhance "
                       "teamwork, communication, and leadership abilities on and off the court.",
        "address": "6100 Main St, Houston, TX 77005, USA",
        "image": None,
    },
    {
        "slug": "community-leadership-coaching",
        "title": "Community Leadership Coaching",
        "tagline": "Mentorship in your community leadership journey.",
        "duration": "1 hr",
        "price": "$70",
        "price_long": "70 US dollars",
        "location": "Main Street",
        "cta": "Book Now",
        "unavailable": None,
        "description": "Receive personalized coaching focusing on developing leadership qualities "
                       "that impact your community positively. Through practical exercises and "
                       "mentorship, learn how to take initiative and lead community projects "
                       "effectively.",
        "address": "6100 Main St, Houston, TX 77005, USA",
        "image": "service-coaching.jpg",
    },
    {
        "slug": "college-mentorship-program",
        "title": "College Mentorship Program",
        "tagline": "Navigate your path to college with expert guidance.",
        "duration": None,
        "price": "$100",
        "price_long": "100 US dollars",
        "location": "Main Street",
        "cta": None,
        "unavailable": "This service is not available, please contact for more information.",
        "description": "Join our College Mentorship Program for personalized guidance through the "
                       "college application process. Benefit from tailored advice on personal "
                       "statements, application forms, and interview preparation to strengthen "
                       "your applications.",
        "address": "6100 Main St, Houston, TX 77005, USA",
        "image": "service-mentorship.jpg",
    },
]

# ----------------------------------------------------------------- blog posts
POSTS = [
    {
        "slug": "leadership-development-for-high-school-students-in-volleyball-program",
        "title": "Leadership Development for High School Students in Volleyball Program",
        "author": "beyondthenethtx",
        "date": "Jun 10, 2025",
        "iso": "2025-06-10",
        "read": "1 min read",
        "image": "post-leadership.jpg",
        "body": [
            "Are you a high school student passionate about volleyball and looking to enhance your "
            "leadership skills? Beyond the Net may just be the perfect opportunity for you!",
            "Founded at Rice University, Beyond the Net is an organization that focuses on mentoring "
            "youth for college and leadership through the sport of volleyball. Their program is "
            "designed to provide individualized college application mentorship to high school "
            "students while also helping them develop crucial leadership qualities that will benefit "
            "them in their future endeavors.",
            "Participating in Beyond the Net's volleyball program not only allows students to improve "
            "their athletic skills but also empowers them to take on leadership roles both on and off "
            "the court. Developing leadership skills during high school not only helps students become "
            "better team players but also sets them apart when it comes time to apply for college.",
            "By joining Beyond the Net, students have the opportunity to engage in community service "
            "projects, take on leadership roles within the program, and build strong relationships with "
            "their peers and mentors. These experiences not only enrich their high school years but "
            "also provide valuable experiences that college admissions officers look for in prospective "
            "students.",
            "If you're interested in joining Beyond the Net's volleyball program, be sure to check out "
            "their website for more information and sign up for this enriching opportunity. Who knows, "
            "this may just be the stepping stone you need to unlock your full potential both on and off "
            "the volleyball court.",
        ],
    },
    {
        "slug": "empowering-youth-for-college-through-volleyball-mentorship",
        "title": "Empowering Youth for College through Volleyball Mentorship",
        "author": "beyondthenethtx",
        "date": "Jun 10, 2025",
        "iso": "2025-06-10",
        "read": "2 min read",
        "image": "post-empowering.jpg",
        "body": [
            "In the realm of youth empowerment and mentorship programs, there lies a uniquely impactful "
            "initiative known as Beyond the Net. This organization, rooted in the love for volleyball, "
            "has blossomed into a beacon of guidance for high school students on their journey towards "
            "college and leadership.",
            "At its core, Beyond the Net stands as a supportive force for young individuals, offering "
            "tailored mentorship for college applications and fostering the growth of leadership skills "
            "within their local communities. By intertwining the passion for volleyball with the pursuit "
            "of higher education, this program not only aids students in achieving their academic dreams "
            "but also equips them with valuable life skills that will serve them well beyond the confines "
            "of a classroom.",
            "Catering to middle and high school students, Beyond the Net has crafted a virtual haven on "
            "their website where interested individuals can effortlessly sign up for the program. "
            "Furthermore, visitors to the site can delve into a wealth of information about the initiative, "
            "gaining insights into its core values and the remarkable work it has accomplished thus far.",
            "Unlike other organizations, Beyond the Net's website has a singular focus – to empower youth "
            "for college through volleyball mentorship. Straying away from conventional aims like "
            "fundraising or merchandise sales, the organization remains steadfast in its mission to uplift "
            "the next generation of leaders and scholars.",
            "As students navigate the tumultuous waters of college applications and personal development, "
            "Beyond the Net stands as a steadfast partner, guiding them towards brighter futures. Through "
            "the transformative power of mentorship and the unity forged in the love for volleyball, this "
            "organization is paving the way for a generation of empowered youth ready to take on the world.",
        ],
    },
    {
        "slug": "transforming-futures-college-prep-and-leadership-program-for-youth",
        "title": "Transforming Futures: College Prep and Leadership Program for Youth",
        "author": "beyondthenethtx",
        "date": "Jun 10, 2025",
        "iso": "2025-06-10",
        "read": "1 min read",
        "image": "post-transforming.jpg",
        "body": [
            "Are you a high school student looking to prepare for college and develop your leadership "
            "skills? If so, there's a fantastic program dedicated to helping you achieve your goals - a "
            "College Prep and Leadership Program for Youth offered by an organization called Beyond the Net.",
            "Based at Rice University, Beyond the Net focuses on mentoring young individuals through the "
            "sport of volleyball. However, their impact goes far beyond the court. They provide "
            "personalized mentorship for the college application process, guiding students through each "
            "step and helping them highlight their leadership qualities and community involvement - all "
            "essential components of a strong college application.",
            "By targeting middle and high school students, Beyond the Net sets out to empower the youth to "
            "grow as leaders within their community. This not only enriches their personal development but "
            "also strengthens their college applications, setting them apart in a competitive applicant pool.",
            "On Beyond the Net's website, you can easily sign up for the program and learn more about how it "
            "can benefit you. You'll find a wealth of information on what the organization has already "
            "accomplished, demonstrating their dedication to transforming the futures of young individuals "
            "through education and leadership.",
            "If you're a student passionate about volleyball and eager to excel in college and beyond, "
            "consider joining Beyond the Net's College Prep and Leadership Program. With their guidance and "
            "support, you'll be well on your way to achieving your academic and leadership goals.",
        ],
    },
]
