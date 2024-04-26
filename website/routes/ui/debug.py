from datetime import datetime, timedelta, timezone
import random
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from ...models.event.event_contributor import EventContributor


from ... import db
from ...orm.user.user import create_user
from ...orm.event.event import create_event
from ...orm.event.event_occurrence import create_event_occurrence
from ...orm.opportunity.opportunity import create_opportunity_post
from ...models.user import User
from ...models.event import Event
from ...models.opportunity import Opportunity, PostType, LocationType, TermType

debug_route = Blueprint("debug", __name__)


@debug_route.route("/debug/", methods=["GET", "POST"])
def debug():
    return render_template("debug.html", user=current_user)


@debug_route.route("/debug/create_demo_users/", methods=["GET", "POST"])
def create_demo_users():
    users = [
        {
            "display_name": "Grace Turner",
            "username": "grace123",
            "email": "grace.turner@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Passionate ballet dancer and choreographer. Loves expressing emotions through movement.",
            "tags": ["ballet", "dancer", "choreographer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/7981bccf-97dd-4be8-384f-07475d937300/public",
            "profile_picture_id": "7981bccf-97dd-4be8-384f-07475d937300",
        },
        {
            "display_name": "Alex Rivera",
            "username": "alex_r",
            "email": "alex.rivera@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Hip-hop enthusiast. Always ready to break it down on the dance floor.",
            "tags": ["hip hop", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/19329467-2c5b-4a52-33de-047689cdbe00/public",
            "profile_picture_id": "19329467-2c5b-4a52-33de-047689cdbe00",
        },
        {
            "display_name": "Luna Vega",
            "username": "lunavega",
            "email": "luna.vega@example.com",
            "password": "password",
            "pronouns": "they/them",
            "bio": "Contemporary dancer with a flair for storytelling. Loves experimenting with movement.",
            "tags": ["contemporary", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/ea5a893f-1053-4199-ec55-7eb289b3e800/public",
            "profile_picture_id": "ea5a893f-1053-4199-ec55-7eb289b3e800",
        },
        {
            "display_name": "Sophia Lee",
            "username": "sophia_dance",
            "email": "sophia.lee@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Classical ballet dancer with a passion for pointe work. Loves performing in story ballets.",
            "tags": ["ballet", "dancer", "choreographer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/86e4dc96-2b64-4a98-23cb-b63c0a738b00/public",
            "profile_picture_id": "86e4dc96-2b64-4a98-23cb-b63c0a738b00",
        },
        {
            "display_name": "Max Vega",
            "username": "maxvega",
            "email": "max.vega@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Versatile dancer skilled in hip-hop, contemporary, and salsa. Choreographs high-energy routines.",
            "tags": ["hip hop", "contemporary", "salsa", "dancer", "choreographer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/db76bfcf-b73c-4751-dc5f-1d7512ffa000/public",
            "profile_picture_id": "db76bfcf-b73c-4751-dc5f-1d7512ffa000",
        },
        {
            "display_name": "Elena Rodriguez",
            "username": "elenarod",
            "email": "elena.rodriguez@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Latin ballroom specialist. Enjoys partnering and competing in international dance events.",
            "tags": ["ballroom", "dancer", "competitor"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/f9974aca-b96d-4083-cbb0-f19c530ea500/public",
            "profile_picture_id": "f9974aca-b96d-4083-cbb0-f19c530ea500",
        },
        {
            "display_name": "Isabella Rodriguez",
            "username": "izzyrod",
            "email": "isabella.rodriguez@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Isabella Rodriguez, a trailblazing force in the dance industry, has dedicated her life to transforming movement into captivating narratives. Known for her ability to fuse different dance styles and evoke powerful emotions through movement, Isabella continues to push the boundaries of artistic expression. With a repertoire of breathtaking performances and a commitment to pushing the art form forward, Isabella Rodriguez stands as a beacon of innovation in the world of dance.",
            "tags": ["choreographer", "artistic director", "contemporary", "indie"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/54af7b3b-9f65-4580-43fb-2f8bdced8600/public",
            "profile_picture_id": "54af7b3b-9f65-4580-43fb-2f8bdced8600",
        },
        {
            "display_name": "Oliver Grant",
            "username": "oliver_g",
            "email": "oliver.grant@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Jazz funk enthusiast. Loves grooving to funky beats and creating dynamic choreography.",
            "tags": ["jazz funk", "dancer", "choreographer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/b21b9ff0-345b-413d-4ba5-4fe4a8550200/public",
            "profile_picture_id": "b21b9ff0-345b-413d-4ba5-4fe4a8550200",
        },
        {
            "display_name": "Maya Patel",
            "username": "mayadance",
            "email": "maya.patel@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Indian classical dancer (Bharatanatyam). Passionate about preserving cultural heritage through dance.",
            "tags": ["Bharatanatyam", "dancer", "cultural"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/19898f7d-bd3d-463f-2e98-9a57afb42b00/public",
            "profile_picture_id": "19898f7d-bd3d-463f-2e98-9a57afb42b00",
        },
        {
            "display_name": "Lucas Martin",
            "username": "lucas_m",
            "email": "lucas.martin@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Tap dancer extraordinaire. Rhythmic footwork and syncopation are my jam!",
            "tags": ["tap", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/3f149449-1be8-4f96-691b-cd999068ba00/public",
            "profile_picture_id": "3f149449-1be8-4f96-691b-cd999068ba00",
        },
        {
            "display_name": "Isabella Wong",
            "username": "isabellaw",
            "email": "isabella.wong@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Contemporary flow artist. Expresses emotions through fluid movement and improvisation.",
            "tags": ["contemporary", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/06d7a73c-57c7-4040-035f-385f2110be00/public",
            "profile_picture_id": "06d7a73c-57c7-4040-035f-385f2110be00",
        },
        {
            "display_name": "David Foster",
            "username": "davidf",
            "email": "david.foster@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Experienced stage manager. Ensures seamless performances behind the scenes.",
            "tags": ["stage manager", "production"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/9734deab-79a9-4121-c341-8c9d2c5d2400/public",
            "profile_picture_id": "9734deab-79a9-4121-c341-8c9d2c5d2400",
        },
        {
            "display_name": "Nina Chen",
            "username": "ninac",
            "email": "nina.chen@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Dance journalist and writer. Chronicles the magic of movement through words.",
            "tags": ["writer", "journalist", "dance"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/e16baa55-0fd9-4219-cacc-3fe7694eb900/public",
            "profile_picture_id": "e16baa55-0fd9-4219-cacc-3fe7694eb900",
        },
        {
            "display_name": "Carlos Ramirez",
            "username": "carlosr",
            "email": "carlos.ramirez@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Salsa instructor and performer. Spreads the joy of Latin dance.",
            "tags": ["salsa", "instructor", "performer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/7271a9f0-0296-44e7-444b-ef7e492dfb00/public",
            "profile_picture_id": "7271a9f0-0296-44e7-444b-ef7e492dfb00",
        },
        {
            "display_name": "Emily Parker",
            "username": "emily_dance",
            "email": "emily.parker@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Versatile dancer trained in jazz, contemporary, and ballroom. Loves performing on stage.",
            "tags": ["jazz", "contemporary", "ballroom", "dancer", "performer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/5f3ee49e-9891-461f-d6b7-fc051e7c2600/public",
            "profile_picture_id": "5f3ee49e-9891-461f-d6b7-fc051e7c2600",
        },
        {
            "display_name": "Leo Kim",
            "username": "leok",
            "email": "leo.kim@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "K-pop dance enthusiast. Choreographs dynamic routines inspired by K-pop idols.",
            "tags": ["K-pop", "choreographer", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/6019ed73-6c7b-45db-55ab-1c64385d1b00/public",
            "profile_picture_id": "6019ed73-6c7b-45db-55ab-1c64385d1b00",
        },
        {
            "display_name": "Aria Patel",
            "username": "ariadance",
            "email": "aria.patel@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Latin fusion dancer. Combines salsa, bachata, and tango for a unique style.",
            "tags": ["salsa", "bachata", "tango", "fusion", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/62d281d7-0099-428a-aca8-0dc31a238700/public",
            "profile_picture_id": "62d281d7-0099-428a-aca8-0dc31a238700",
        },
        {
            "display_name": "Evan Foster",
            "username": "evanf",
            "email": "evan.foster@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Lighting and sound technician. Ensures dazzling performances with perfect cues.",
            "tags": ["stage manager", "technician", "production"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/58bb2524-dd85-439c-8bd4-b535ad7c7100/public",
            "profile_picture_id": "58bb2524-dd85-439c-8bd4-b535ad7c7100",
        },
        {
            "display_name": "Zara Liu",
            "username": "zaral",
            "email": "zara.liu@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Bollywood dance lover. Spreads joy through vibrant and energetic routines.",
            "tags": ["Bollywood", "dancer", "enthusiast"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/4c22f0a1-2f94-45a5-3f7c-8e94452c5000/public",
            "profile_picture_id": "4c22f0a1-2f94-45a5-3f7c-8e94452c5000",
        },
        {
            "display_name": "Samuel Rodriguez",
            "username": "samuelr",
            "email": "samuel.rodriguez@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Breakdancer (b-boy). Pops, locks, and spins to the beat!",
            "tags": ["breakdance", "b-boy", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/261fd1ec-e27c-4976-ebb3-4b53a68ea300/public",
            "profile_picture_id": "261fd1ec-e27c-4976-ebb3-4b53a68ea300",
        },
        {
            "display_name": "Lila Chen",
            "username": "lilac",
            "email": "lila.chen@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Experimental movement artist. Pushes boundaries and challenges norms.",
            "tags": ["experimental", "movement", "artist"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/264ee902-52dc-499f-b5d6-f094ee669500/public",
            "profile_picture_id": "264ee902-52dc-499f-b5d6-f094ee669500",
        },
        {
            "display_name": "Daniel Wong",
            "username": "danielw",
            "email": "daniel.wong@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Contemporary ballet dancer. Melds classical technique with modern expression.",
            "tags": ["contemporary ballet", "dancer"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/1177b290-79c2-4c7c-5cd9-0d2ea7467700/public",
            "profile_picture_id": "1177b290-79c2-4c7c-5cd9-0d2ea7467700",
        },
        {
            "display_name": "Mia Johnson",
            "username": "miaj",
            "email": "mia.johnson@example.com",
            "password": "password",
            "pronouns": "she/her",
            "bio": "Urban dance advocate. Empowers youth through hip-hop workshops.",
            "tags": ["hip hop", "urban", "advocate", "teacher"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/8609a02a-1e6e-4c8e-b886-8a670e5be500/public",
            "profile_picture_id": "8609a02a-1e6e-4c8e-b886-8a670e5be500",
        },
        {
            "display_name": "Oscar Morales",
            "username": "oscarm",
            "email": "oscar.morales@example.com",
            "password": "password",
            "pronouns": "he/him",
            "bio": "Salsa social dancer. Spins partners with flair and infectious energy.",
            "tags": ["salsa", "social dancer", "enthusiast"],
            "profile_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/6a779dec-8414-48dd-8615-bfbb7971a700/public",
            "profile_picture_id": "6a779dec-8414-48dd-8615-bfbb7971a700",
        },
    ]
    # users = [
    #     {
    #         "display_name": "Grace Turner",
    #         "username": "grace123",
    #         "email": "grace.turner@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Passionate ballet dancer and choreographer. Loves expressing emotions through movement.",
    #         "tags": ["ballet", "dancer", "choreographer"]
    #     },
    #     {
    #         "display_name": "Alex Rivera",
    #         "username": "alex_r",
    #         "email": "alex.rivera@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Hip-hop enthusiast. Always ready to break it down on the dance floor.",
    #         "tags": ["hip hop", "dancer"]
    #     },
    #     {
    #         "display_name": "Luna Vega",
    #         "username": "lunavega",
    #         "email": "luna.vega@example.com",
    #         "password": "password",
    #         "pronouns": "they/them",
    #         "bio": "Contemporary dancer with a flair for storytelling. Loves experimenting with movement.",
    #         "tags": ["contemporary", "dancer"]
    #     },
    #     {
    #         "display_name": "Sophia Lee",
    #         "username": "sophia_dance",
    #         "email": "sophia.lee@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Classical ballet dancer with a passion for pointe work. Loves performing in story ballets.",
    #         "tags": ["ballet", "dancer", "choreographer"]
    #     },
    #     {
    #         "display_name": "Max Vega",
    #         "username": "maxvega",
    #         "email": "max.vega@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Versatile dancer skilled in hip-hop, contemporary, and salsa. Choreographs high-energy routines.",
    #         "tags": ["hip hop", "contemporary", "salsa", "dancer", "choreographer"]
    #     },
    #     {
    #         "display_name": "Elena Rodriguez",
    #         "username": "elenarod",
    #         "email": "elena.rodriguez@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Latin ballroom specialist. Enjoys partnering and competing in international dance events.",
    #         "tags": ["ballroom", "dancer", "competitor"]
    #     },
    #     {
    #         "display_name": "Isabella Rodriguez",
    #         "username": "izzyrod",
    #         "email": "isabella.rodriguez@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Isabella Rodriguez, a trailblazing force in the dance industry, has dedicated her life to transforming movement into captivating narratives. Known for her ability to fuse different dance styles and evoke powerful emotions through movement, Isabella continues to push the boundaries of artistic expression. With a repertoire of breathtaking performances and a commitment to pushing the art form forward, Isabella Rodriguez stands as a beacon of innovation in the world of dance.",
    #         "tags": ["choreographer", "artistic director", "contemporary", "indie"]
    #     },
    #     {
    #         "display_name": "Oliver Grant",
    #         "username": "oliver_g",
    #         "email": "oliver.grant@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Jazz funk enthusiast. Loves grooving to funky beats and creating dynamic choreography.",
    #         "tags": ["jazz funk", "dancer", "choreographer"]
    #     },
    #     {
    #         "display_name": "Maya Patel",
    #         "username": "mayadance",
    #         "email": "maya.patel@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Indian classical dancer (Bharatanatyam). Passionate about preserving cultural heritage through dance.",
    #         "tags": ["Bharatanatyam", "dancer", "cultural"]
    #     },
    #     {
    #         "display_name": "Lucas Martin",
    #         "username": "lucas_m",
    #         "email": "lucas.martin@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Tap dancer extraordinaire. Rhythmic footwork and syncopation are my jam!",
    #         "tags": ["tap", "dancer"]
    #     },
    #     {
    #         "display_name": "Isabella Wong",
    #         "username": "isabellaw",
    #         "email": "isabella.wong@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Contemporary flow artist. Expresses emotions through fluid movement and improvisation.",
    #         "tags": ["contemporary", "dancer"]
    #     },
    #     {
    #         "display_name": "David Foster",
    #         "username": "davidf",
    #         "email": "david.foster@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Experienced stage manager. Ensures seamless performances behind the scenes.",
    #         "tags": ["stage manager", "production"]
    #     },
    #     {
    #         "display_name": "Nina Chen",
    #         "username": "ninac",
    #         "email": "nina.chen@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Dance journalist and writer. Chronicles the magic of movement through words.",
    #         "tags": ["writer", "journalist", "dance"]
    #     },
    #     {
    #         "display_name": "Carlos Ramirez",
    #         "username": "carlosr",
    #         "email": "carlos.ramirez@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Salsa instructor and performer. Spreads the joy of Latin dance.",
    #         "tags": ["salsa", "instructor", "performer"]
    #     },
    #     {
    #         "display_name": "Emily Parker",
    #         "username": "emily_dance",
    #         "email": "emily.parker@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Versatile dancer trained in jazz, contemporary, and ballroom. Loves performing on stage.",
    #         "tags": ["jazz", "contemporary", "ballroom", "dancer", "performer"]
    #     },
    #     {
    #         "display_name": "Leo Kim",
    #         "username": "leok",
    #         "email": "leo.kim@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "K-pop dance enthusiast. Choreographs dynamic routines inspired by K-pop idols.",
    #         "tags": ["K-pop", "choreographer", "dancer"]
    #     },
    #     {
    #         "display_name": "Aria Patel",
    #         "username": "ariadance",
    #         "email": "aria.patel@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Latin fusion dancer. Combines salsa, bachata, and tango for a unique style.",
    #         "tags": ["salsa", "bachata", "tango", "fusion", "dancer"]
    #     },
    #     {
    #         "display_name": "Evan Foster",
    #         "username": "evanf",
    #         "email": "evan.foster@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Lighting and sound technician. Ensures dazzling performances with perfect cues.",
    #         "tags": ["stage manager", "technician", "production"]
    #     },
    #     {
    #         "display_name": "Zara Liu",
    #         "username": "zaral",
    #         "email": "zara.liu@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Bollywood dance lover. Spreads joy through vibrant and energetic routines.",
    #         "tags": ["Bollywood", "dancer", "enthusiast"]
    #     },
    #     {
    #         "display_name": "Samuel Rodriguez",
    #         "username": "samuelr",
    #         "email": "samuel.rodriguez@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Breakdancer (b-boy). Pops, locks, and spins to the beat!",
    #         "tags": ["breakdance", "b-boy", "dancer"]
    #     },
    #     {
    #         "display_name": "Lila Chen",
    #         "username": "lilac",
    #         "email": "lila.chen@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Experimental movement artist. Pushes boundaries and challenges norms.",
    #         "tags": ["experimental", "movement", "artist"]
    #     },
    #     {
    #         "display_name": "Daniel Wong",
    #         "username": "danielw",
    #         "email": "daniel.wong@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Contemporary ballet dancer. Melds classical technique with modern expression.",
    #         "tags": ["contemporary ballet", "dancer"]
    #     },
    #     {
    #         "display_name": "Mia Johnson",
    #         "username": "miaj",
    #         "email": "mia.johnson@example.com",
    #         "password": "password",
    #         "pronouns": "she/her",
    #         "bio": "Urban dance advocate. Empowers youth through hip-hop workshops.",
    #         "tags": ["hip hop", "urban", "advocate", "teacher"]
    #     },
    #     {
    #         "display_name": "Oscar Morales",
    #         "username": "oscarm",
    #         "email": "oscar.morales@example.com",
    #         "password": "password",
    #         "pronouns": "he/him",
    #         "bio": "Salsa social dancer. Spins partners with flair and infectious energy.",
    #         "tags": ["salsa", "social dancer", "enthusiast"]
    #     }
    # ]

    for user in users:
        response = create_user(
            username=user["username"],
            email=user["email"],
            password=user["password"] + "@A1",
            display_name=user["display_name"],
            pronouns=user["pronouns"],
            bio=user["bio"],
            tags=user["tags"],
            profile_picture_id=user["profile_picture_id"],
            profile_picture_url=user["profile_picture_url"],
        )
        if response["status_code"] != 201:
            print(response["status_code"])
            print(response["message"])
            print(response["data"])
        else:
            db.session.add(response["data"])
            db.session.commit()

    return redirect(url_for("people.people_list"))


@debug_route.route("/debug/create_demo_events/", methods=["GET", "POST"])
def create_demo_events():

    events = [
        {
            "title": "Latin Rhythms Fiesta",
            "description": "Get ready to salsa, bachata, and cha-cha! A lively celebration of Latin dance and music.",
            "url": "https://www.latinrhythmsfiesta.com",
            "tags": ["salsa", "bachata", "Latin", "dance"],
            "venue_name": "Casa de Sabor",
            "venue_address": "456 Salsa Avenue, Toronto, ON M4X 1Y8",
            "venue_is_mobility_aid_accessible": False,
            "accessibility_notes": "Please note that the venue has stairs and is not wheelchair accessible.",
            "min_ticket_price": 15.0,
            "max_ticket_price": 35.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/d0d8dd48-4606-4feb-2325-343ea9f75d00/public",
            "image_picture_id": "d0d8dd48-4606-4feb-2325-343ea9f75d00",
        },
        {
            "title": "Urban Groove Showcase",
            "description": "A high-energy showcase featuring urban dance crews from across the GTA. Hip-hop, popping, and locking at its finest!",
            "url": "https://www.urbangrooveshowcase.com",
            "tags": ["hip hop", "urban", "dance", "showcase"],
            "venue_name": "Metro Arts Center",
            "venue_address": "789 Beat Street, Mississauga, ON L5R 2T3",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "The venue has accessible entrances and seating. No strobe lights during the performance.",
            "min_ticket_price": 25.0,
            "max_ticket_price": 60.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/3f1b2b07-534a-43f5-5187-16045379b400/public",
            "image_picture_id": "3f1b2b07-534a-43f5-5187-16045379b400",
        },
        {
            "title": "Before You're Gone",
            "description": "“Before You’re Gone” is a poignant contemporary dance routine that captures the essence of fleeting moments and the tender ache of farewells. Performed by a solo female dancer, the piece unfolds on a dimly lit stage, where her silhouette weaves through the shadows. Her movements are a painting of love, loss, and the bittersweet beauty of final goodbyes. As the music swells, her dance intensifies, embodying the urgency and intensity of time slipping away, leaving the audience with a haunting reminder to hold close what is dear, “Before You’re Gone”.",
            "url": "https://www.beforeyouregone.com/",
            "tags": ["contemporary", "solo dancer", "emotional"],
            "venue_name": "Young Centre for the Performing Arts",
            "venue_address": "50 Tank House Lane, Toronto, ON M5A 3C4",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Strobe lighting will be used in the first 5 minutes of the performance, except for the Thursday performances. There will be dimmed lighting during all performances.",
            "min_ticket_price": 20.0,
            "max_ticket_price": 40.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/8b5b2a05-f809-463b-0e0f-c0d97e93dd00/public",
            "image_picture_id": "8b5b2a05-f809-463b-0e0f-c0d97e93dd00",
        },
        {
            "title": "Introductory Tap Workshop",
            "description": "Passionate Argentine tango performances and social dancing. Feel the romance and intensity of this captivating dance form.",
            "url": "https://www.tangonights.com",
            "tags": ["tango", "Argentine", "dance", "passion"],
            "venue_name": "Café Milonga",
            "venue_address": "567 Embrace Avenue, Toronto, ON M6G 1X2",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "The venue is wheelchair accessible. Dimmed lighting during performances.",
            "min_ticket_price": 30.0,
            "max_ticket_price": 80.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/669ddc52-ca92-45f9-13a6-1c1460de7500/public",
            "image_picture_id": "669ddc52-ca92-45f9-13a6-1c1460de7500",
        },
        {
            "title": "Bollywood Beats Festival",
            "description": "A vibrant celebration of Bollywood dance, music, and culture. Get ready to move to the rhythm of India!",
            "url": "https://www.bollywoodbeatsfest.com",
            "tags": ["Bollywood", "Indian", "dance", "festival"],
            "venue_name": "Rangoli Pavilion",
            "venue_address": "234 Sitar Lane, Brampton, ON L6P 3H5",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Accessible entrance on the west side of the venue. No strobes or intense flashing lights.",
            "min_ticket_price": 20.0,
            "max_ticket_price": 50.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/452bbda4-4796-49d3-34bc-e9d8edb26900/public",
            "image_picture_id": "452bbda4-4796-49d3-34bc-e9d8edb26900",
        },
        {
            "title": "Contemporary Collisions",
            "description": "An experimental showcase blending contemporary dance with multimedia art. Prepare for thought-provoking performances.",
            "url": "https://www.contemporarycollisions.com",
            "tags": ["contemporary", "experimental", "dance", "art"],
            "venue_name": "Gallery X",
            "venue_address": "345 Canvas Avenue, Toronto, ON M4S 2W9",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Wheelchair ramps available. Minimal use of flashing lights.",
            "min_ticket_price": 25.0,
            "max_ticket_price": 70.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/74df0e4a-24fc-4d6d-cc5c-54a98bcb4600/public",
            "image_picture_id": "74df0e4a-24fc-4d6d-cc5c-54a98bcb4600",
        },
        {
            "title": "Salsa Sunset Social",
            "description": "Dance the night away to sizzling salsa beats by the waterfront. Beginners and pros welcome!",
            "url": "https://www.salsasunset.com",
            "tags": ["salsa", "Latin", "dance", "social"],
            "venue_name": "Harbourview Pavilion",
            "venue_address": "123 Salsa Bay, Toronto, ON M5J 2T4",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Accessible pathways to the venue. No strobe lights during the social dance.",
            "min_ticket_price": 15.0,
            "max_ticket_price": 40.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/e640a6cf-ffc9-486b-2176-b8a4d34b2700/public",
            "image_picture_id": "e640a6cf-ffc9-486b-2176-b8a4d34b2700",
        },
        {
            "title": "Fusion Fireworks",
            "description": "A mesmerizing blend of classical Indian dance, contemporary movement, and fire spinning. Prepare to be amazed!",
            "url": "https://www.fusionfireworks.com",
            "tags": ["Indian dance", "contemporary", "fire spinning", "spectacle"],
            "venue_name": "Firefly Gardens",
            "venue_address": "789 Flame Avenue, Markham, ON L3R 5T2",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Accessible pathways throughout the venue. Fire performance is outdoors.",
            "min_ticket_price": 25.0,
            "max_ticket_price": 60.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/b506bb00-5e73-40e0-a5c7-809db8b58800/public",
            "image_picture_id": "b506bb00-5e73-40e0-a5c7-809db8b58800",
        },
        {
            "title": "Ballet in the Park",
            "description": "An enchanting outdoor ballet performance set against a natural backdrop. Bring a picnic blanket and enjoy the artistry.",
            "url": "https://www.balletinthepark.com",
            "tags": ["ballet", "outdoor", "nature", "performance"],
            "venue_name": "Sunset Meadow",
            "venue_address": "123 Tutu Trail, Vaughan, ON L4J 8K9",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Accessible parking available. No sudden lighting changes during the show.",
            "min_ticket_price": 15.0,
            "max_ticket_price": 35.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/d8b80192-b3c4-416b-8273-aa442d51d500/public",
            "image_picture_id": "d8b80192-b3c4-416b-8273-aa442d51d500",
        },
        {
            "title": "Break the Beat Battle",
            "description": "Witness jaw-dropping breakdance battles as crews battle it out for supremacy. Who will break the beat?",
            "url": "https://www.breakthebeatbattle.com",
            "tags": ["breakdance", "b-boy", "competition", "street dance"],
            "venue_name": "Concrete Arena",
            "venue_address": "456 Break Street, Scarborough, ON M1B 2C3",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Accessible seating available. No intense strobes during battles.",
            "min_ticket_price": 10.0,
            "max_ticket_price": 25.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/84f5bb90-21ef-4665-844a-d75998ed1e00/public",
            "image_picture_id": "84f5bb90-21ef-4665-844a-d75998ed1e00",
        },
        {
            "title": "Flamenco Fiesta",
            "description": "Passionate flamenco performances accompanied by live guitar music. Olé!",
            "url": "https://www.flamencofiesta.com",
            "tags": ["flamenco", "Spanish", "dance", "passion"],
            "venue_name": "Casa del Flamenco",
            "venue_address": "234 Sevillana Street, Richmond Hill, ON L4S 1T5",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Wheelchair ramps at the entrance. No sudden light changes during performances.",
            "min_ticket_price": 30.0,
            "max_ticket_price": 70.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/60714456-0994-45ee-1844-4a8f6e84f100/public",
            "image_picture_id": "60714456-0994-45ee-1844-4a8f6e84f100",
        },
        {
            "title": "Rhythm Revival",
            "description": "A soulful evening of tap dance, live jazz, and spoken word. Celebrate the art of rhythm!",
            "url": "https://www.rhythmrevival.com",
            "tags": ["tap", "jazz", "spoken word", "performance"],
            "venue_name": "Harmony Hall",
            "venue_address": "789 Sync Street, Etobicoke, ON M9B 2T1",
            "venue_is_mobility_aid_accessible": True,
            "accessibility_notes": "Accessible seating available. No sudden light changes during performances.",
            "min_ticket_price": 20.0,
            "max_ticket_price": 55.0,
            "image_picture_url": "https://imagedelivery.net/ieKvjIrSdSi118m2pamc8g/3d3a4c20-e2c0-4d34-73da-f14042023f00/public",
            "image_picture_id": "3d3a4c20-e2c0-4d34-73da-f14042023f00",
        },
    ]

    # events = [
    #     # {
    #     #     "title": "Groove Fusion Night",
    #     #     "description": "An electrifying fusion of hip-hop, jazz, and contemporary dance styles. Join us for a night of rhythm and movement!",
    #     #     "url": "https://www.groovefusionnight.com",
    #     #     "tags": ["hip hop", "jazz", "contemporary", "dance"],
    #     #     "venue_name": "Toronto Dance Hub",
    #     #     "venue_address": "123 Groove Street, Toronto, ON M5V 2W6",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "The venue has ramps and an elevator for wheelchair access. No strobe lights during the performance.",
    #     #     "min_ticket_price": 20.0,
    #     #     "max_ticket_price": 50.0
    #     # },
    #     {
    #         "title": "Latin Rhythms Fiesta",
    #         "description": "Get ready to salsa, bachata, and cha-cha! A lively celebration of Latin dance and music.",
    #         "url": "https://www.latinrhythmsfiesta.com",
    #         "tags": ["salsa", "bachata", "Latin", "dance"],
    #         "venue_name": "Casa de Sabor",
    #         "venue_address": "456 Salsa Avenue, Toronto, ON M4X 1Y8",
    #         "venue_is_mobility_aid_accessible": False,
    #         "accessibility_notes": "Please note that the venue has stairs and is not wheelchair accessible.",
    #         "min_ticket_price": 15.0,
    #         "max_ticket_price": 35.0,
    #     },
    #     {
    #         "title": "Urban Groove Showcase",
    #         "description": "A high-energy showcase featuring urban dance crews from across the GTA. Hip-hop, popping, and locking at its finest!",
    #         "url": "https://www.urbangrooveshowcase.com",
    #         "tags": ["hip hop", "urban", "dance", "showcase"],
    #         "venue_name": "Metro Arts Center",
    #         "venue_address": "789 Beat Street, Mississauga, ON L5R 2T3",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "The venue has accessible entrances and seating. No strobe lights during the performance.",
    #         "min_ticket_price": 25.0,
    #         "max_ticket_price": 60.0,
    #     },
    #     {
    #         "title": "Before You're Gone",
    #         "description": "“Before You’re Gone” is a poignant contemporary dance routine that captures the essence of fleeting moments and the tender ache of farewells. Performed by a solo female dancer, the piece unfolds on a dimly lit stage, where her silhouette weaves through the shadows. Her movements are a painting of love, loss, and the bittersweet beauty of final goodbyes. As the music swells, her dance intensifies, embodying the urgency and intensity of time slipping away, leaving the audience with a haunting reminder to hold close what is dear, “Before You’re Gone”.",
    #         "url": "https://www.beforeyouregone.com/",
    #         "tags": ["contemporary", "solo dancer", "emotional"],
    #         "venue_name": "Young Centre for the Performing Arts",
    #         "venue_address": "50 Tank House Lane, Toronto, ON M5A 3C4",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Strobe lighting will be used in the first 5 minutes of the performance, except for the Thursday performances. There will be dimmed lighting during all performances.",
    #         "min_ticket_price": 20.0,
    #         "max_ticket_price": 40.0,
    #     },
    #     {
    #         "title": "Introductory Tap Workshop",
    #         "description": "Passionate Argentine tango performances and social dancing. Feel the romance and intensity of this captivating dance form.",
    #         "url": "https://www.tangonights.com",
    #         "tags": ["tango", "Argentine", "dance", "passion"],
    #         "venue_name": "Café Milonga",
    #         "venue_address": "567 Embrace Avenue, Toronto, ON M6G 1X2",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "The venue is wheelchair accessible. Dimmed lighting during performances.",
    #         "min_ticket_price": 30.0,
    #         "max_ticket_price": 80.0,
    #     },
    #     # {
    #     #     "title": "Tango Nights",
    #     #     "description": "Passionate Argentine tango performances and social dancing. Feel the romance and intensity of this captivating dance form.",
    #     #     "url": "https://www.tangonights.com",
    #     #     "tags": ["tango", "Argentine", "dance", "passion"],
    #     #     "venue_name": "Café Milonga",
    #     #     "venue_address": "567 Embrace Avenue, Toronto, ON M6G 1X2",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "The venue is wheelchair accessible. Dimmed lighting during performances.",
    #     #     "min_ticket_price": 30.0,
    #     #     "max_ticket_price": 80.0
    #     # },
    #     {
    #         "title": "Bollywood Beats Festival",
    #         "description": "A vibrant celebration of Bollywood dance, music, and culture. Get ready to move to the rhythm of India!",
    #         "url": "https://www.bollywoodbeatsfest.com",
    #         "tags": ["Bollywood", "Indian", "dance", "festival"],
    #         "venue_name": "Rangoli Pavilion",
    #         "venue_address": "234 Sitar Lane, Brampton, ON L6P 3H5",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Accessible entrance on the west side of the venue. No strobes or intense flashing lights.",
    #         "min_ticket_price": 20.0,
    #         "max_ticket_price": 50.0,
    #     },
    #     {
    #         "title": "Contemporary Collisions",
    #         "description": "An experimental showcase blending contemporary dance with multimedia art. Prepare for thought-provoking performances.",
    #         "url": "https://www.contemporarycollisions.com",
    #         "tags": ["contemporary", "experimental", "dance", "art"],
    #         "venue_name": "Gallery X",
    #         "venue_address": "345 Canvas Avenue, Toronto, ON M4S 2W9",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Wheelchair ramps available. Minimal use of flashing lights.",
    #         "min_ticket_price": 25.0,
    #         "max_ticket_price": 70.0,
    #     },
    #     {
    #         "title": "Salsa Sunset Social",
    #         "description": "Dance the night away to sizzling salsa beats by the waterfront. Beginners and pros welcome!",
    #         "url": "https://www.salsasunset.com",
    #         "tags": ["salsa", "Latin", "dance", "social"],
    #         "venue_name": "Harbourview Pavilion",
    #         "venue_address": "123 Salsa Bay, Toronto, ON M5J 2T4",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Accessible pathways to the venue. No strobe lights during the social dance.",
    #         "min_ticket_price": 15.0,
    #         "max_ticket_price": 40.0,
    #     },
    #     {
    #         "title": "Fusion Fireworks",
    #         "description": "A mesmerizing blend of classical Indian dance, contemporary movement, and fire spinning. Prepare to be amazed!",
    #         "url": "https://www.fusionfireworks.com",
    #         "tags": ["Indian dance", "contemporary", "fire spinning", "spectacle"],
    #         "venue_name": "Firefly Gardens",
    #         "venue_address": "789 Flame Avenue, Markham, ON L3R 5T2",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Accessible pathways throughout the venue. Fire performance is outdoors.",
    #         "min_ticket_price": 25.0,
    #         "max_ticket_price": 60.0,
    #     },
    #     # {
    #     #     "title": "Swingin' Soiree",
    #     #     "description": "Step back in time with swing dance classics! Live jazz band, vintage attire, and swing lessons for all.",
    #     #     "url": "https://www.swinginsoiree.com",
    #     #     "tags": ["swing", "jazz", "vintage", "dance party"],
    #     #     "venue_name": "Retro Ballroom",
    #     #     "venue_address": "567 Swing Street, Toronto, ON M6H 4R7",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "The venue has ramps and an accessible restroom. No strobe lights during the event.",
    #     #     "min_ticket_price": 20.0,
    #     #     "max_ticket_price": 45.0
    #     # },
    #     {
    #         "title": "Ballet in the Park",
    #         "description": "An enchanting outdoor ballet performance set against a natural backdrop. Bring a picnic blanket and enjoy the artistry.",
    #         "url": "https://www.balletinthepark.com",
    #         "tags": ["ballet", "outdoor", "nature", "performance"],
    #         "venue_name": "Sunset Meadow",
    #         "venue_address": "123 Tutu Trail, Vaughan, ON L4J 8K9",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Accessible parking available. No sudden lighting changes during the show.",
    #         "min_ticket_price": 15.0,
    #         "max_ticket_price": 35.0,
    #     },
    #     {
    #         "title": "Break the Beat Battle",
    #         "description": "Witness jaw-dropping breakdance battles as crews battle it out for supremacy. Who will break the beat?",
    #         "url": "https://www.breakthebeatbattle.com",
    #         "tags": ["breakdance", "b-boy", "competition", "street dance"],
    #         "venue_name": "Concrete Arena",
    #         "venue_address": "456 Break Street, Scarborough, ON M1B 2C3",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Accessible seating available. No intense strobes during battles.",
    #         "min_ticket_price": 10.0,
    #         "max_ticket_price": 25.0,
    #     },
    #     {
    #         "title": "Flamenco Fiesta",
    #         "description": "Passionate flamenco performances accompanied by live guitar music. Olé!",
    #         "url": "https://www.flamencofiesta.com",
    #         "tags": ["flamenco", "Spanish", "dance", "passion"],
    #         "venue_name": "Casa del Flamenco",
    #         "venue_address": "234 Sevillana Street, Richmond Hill, ON L4S 1T5",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Wheelchair ramps at the entrance. No sudden light changes during performances.",
    #         "min_ticket_price": 30.0,
    #         "max_ticket_price": 70.0,
    #     },
    #     {
    #         "title": "Rhythm Revival",
    #         "description": "A soulful evening of tap dance, live jazz, and spoken word. Celebrate the art of rhythm!",
    #         "url": "https://www.rhythmrevival.com",
    #         "tags": ["tap", "jazz", "spoken word", "performance"],
    #         "venue_name": "Harmony Hall",
    #         "venue_address": "789 Sync Street, Etobicoke, ON M9B 2T1",
    #         "venue_is_mobility_aid_accessible": True,
    #         "accessibility_notes": "Accessible seating available. No sudden light changes during performances.",
    #         "min_ticket_price": 20.0,
    #         "max_ticket_price": 55.0,
    #     },
    #     # {
    #     #     "title": "Fusion Flow Fest",
    #     #     "description": "Explore the intersection of contemporary dance and flow arts (poi, hoops, fans). A mesmerizing fusion!",
    #     #     "url": "https://www.fusionflowfest.com",
    #     #     "tags": ["contemporary", "flow arts", "dance", "fusion"],
    #     #     "venue_name": "Flowtopia Studio",
    #     #     "venue_address": "567 Flow Lane, North York, ON M3C 1R7",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "Accessible entrance on the east side of the studio. Flow arts are performed with LED props.",
    #     #     "min_ticket_price": 25.0,
    #     #     "max_ticket_price": 65.0
    #     # },
    #     # {
    #     #     "title": "Ballet Under the Stars",
    #     #     "description": "An enchanting outdoor ballet performance set against the backdrop of a starlit sky. Pure magic!",
    #     #     "url": "https://www.balletunderthestars.com",
    #     #     "tags": ["ballet", "outdoor", "starry night", "performance"],
    #     #     "venue_name": "Celestial Park",
    #     #     "venue_address": "123 Starlight Avenue, Richmond Hill, ON L4E 5T6",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "Accessible pathways throughout the park. No intense lighting changes during the show.",
    #     #     "min_ticket_price": 15.0,
    #     #     "max_ticket_price": 40.0
    #     # },
    #     # {
    #     #     "title": "Latin Groove Carnival",
    #     #     "description": "Salsa, merengue, and cumbia galore! A lively celebration of Latin dance and music.",
    #     #     "url": "https://www.latingroovecarnival.com",
    #     #     "tags": ["salsa", "merengue", "cumbia", "fiesta"],
    #     #     "venue_name": "Carnaval Ballroom",
    #     #     "venue_address": "456 Sabor Street, Vaughan, ON L6A 1T2",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "The venue has ramps and an accessible restroom. No strobe lights during the fiesta.",
    #     #     "min_ticket_price": 20.0,
    #     #     "max_ticket_price": 50.0
    #     # },
    #     # {
    #     #     "title": "Jazz Jam Session",
    #     #     "description": "An intimate evening of live jazz music and improvised dance. Bring your swing and join the jam!",
    #     #     "url": "https://www.jazzjamsession.com",
    #     #     "tags": ["jazz", "improvisation", "music", "jam"],
    #     #     "venue_name": "Blue Note Lounge",
    #     #     "venue_address": "234 Jazz Avenue, Toronto, ON M5V 3R8",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "Accessible seating available. No intense lighting changes during the session.",
    #     #     "min_ticket_price": 18.0,
    #     #     "max_ticket_price": 45.0
    #     # },
    #     # {
    #     #     "title": "Salsa Sunset Cruise",
    #     #     "description": "Sail the Toronto Harbor while dancing to sizzling salsa beats. A unique dance experience on the water!",
    #     #     "url": "https://www.salsasunsetcruise.com",
    #     #     "tags": ["salsa", "Latin", "dance party"],
    #     #     "venue_name": "Salsa Yacht",
    #     #     "venue_address": "Pier 123, Toronto Harbor, ON M5J 1A7",
    #     #     "venue_is_mobility_aid_accessible": False,
    #     #     "accessibility_notes": "The yacht has stairs and is not wheelchair accessible. No strobe lights during the cruise.",
    #     #     "min_ticket_price": 30.0,
    #     #     "max_ticket_price": 75.0
    #     # },
    #     # {
    #     #     "title": "Flamenco Fusion Showcase",
    #     #     "description": "Flamenco meets contemporary and electronic music. A fiery blend of tradition and innovation.",
    #     #     "url": "https://www.flamencofusion.com",
    #     #     "tags": ["flamenco", "contemporary", "fusion", "performance"],
    #     #     "venue_name": "Tablao Flamenco",
    #     #     "venue_address": "234 Flamenco Avenue, Vaughan, ON L6A 2S7",
    #     #     "venue_is_mobility_aid_accessible": True,
    #     #     "accessibility_notes": "Wheelchair ramps available. No intense strobes during the showcase.",
    #     #     "min_ticket_price": 25.0,
    #     #     "max_ticket_price": 60.0
    #     # }
    # ]

    users = db.session.query(User).all()
    for event in events:
        new_event: Event = create_event(
            organizer=random.choice(users),
            title=event["title"],
            description=event["description"],
            url=event["url"],
            tags=event["tags"],
            venue_name=event["venue_name"],
            venue_address=event["venue_address"],
            venue_is_mobility_aid_accessible=event["venue_is_mobility_aid_accessible"],
            accessibility_notes=event["accessibility_notes"],
            min_ticket_price=event["min_ticket_price"],
            max_ticket_price=event["max_ticket_price"],
            occurrences=list(),
            contributors=list(),
            commit_db_after_creation=False,
            image_picture_url=event["image_picture_url"],
            image_picture_id=event["image_picture_id"],
        )["data"]
        db.session.add(new_event)

        end_time = datetime.now() + timedelta(hours=random.randint(1, 4320))
        for _ in range(1, random.randint(1, 10)):
            start_time = end_time + timedelta(hours=random.randint(1, 168))
            end_time = start_time + timedelta(minutes=random.randint(15, 180))
            is_relaxed_performance = bool(random.getrandbits(1))
            is_photosensitivity_friendly = bool(random.getrandbits(1))
            is_hearing_accessible = bool(random.getrandbits(1))
            is_visually_accessible = bool(random.getrandbits(1))
            create_event_occurrence(
                event=new_event,
                start_time=start_time,
                end_time=end_time,
                is_relaxed_performance=is_relaxed_performance,
                is_photosensitivity_friendly=is_photosensitivity_friendly,
                is_hearing_accessible=is_hearing_accessible,
                is_visually_accessible=is_visually_accessible,
                commit_db_after_creation=False,
            )["data"]

        for _ in range(1, random.randint(0, 10)):
            new_contributor = EventContributor(
                event_id=new_event.id,
                user_id=random.choice(users).id,
                role="Contributor",
            )
            db.session.add(new_contributor)

    db.session.commit()
    return redirect(url_for("events.events_list"))


@debug_route.route("/debug/create_demo_opportunities/", methods=["GET", "POST"])
def create_demo_opportunities():
    dance_tags = [
        "Contemporary",
        "BalletLife",
        "HipHopCulture",
        "JazzMoves",
        "TapLife",
        "BallroomStyle",
        "LatinVibes",
        "StreetCulture",
        "ModernArt",
        "BreakLife",
        "FusionStyle",
        "CulturalExpressions",
        "SalsaPassion",
        "FlamencoLife",
        "SwingRhythms",
    ]

    locations = [
        "Toronto Dance Theatre, Toronto",
        "The National Ballet School, Toronto",
        "DanceLife X Centre, Toronto",
        "Joy of Dance Centre, Toronto",
        "City Dance Corps, Toronto",
        "The Underground Dance Centre, Toronto",
        "Metro Movement Dance Studio, Toronto",
    ]

    def getRandVals(vals) -> list[str]:
        no_tags = random.randint(0, 5)
        return [random.choice(vals) for _ in range(no_tags)]

    posts = [
        {
            "type": PostType.AUDITION,
            "title": "Rhythmic Fusion Showcase",
            "organizer": "National Ballet",
            "closing_date": datetime.now(timezone.utc)
            + timedelta(days=random.randint(15, 130)),
            "tags": getRandVals(dance_tags),
            "location_type": LocationType.IN_PERSON,
            "location": random.choice(locations),
            "start_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(5, 15)),
            "end_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(17, 80)),
            "is_paid": True,
            "pay": "2 cents",
            "term_type": TermType.FULL_TIME,
            "number_positions": random.choice([None, 1, 2, 4, 8, 11]),
            "description": "Easy Audition",
            "responsibilities": "Dance well",
            "requirements": "None",
            "compensation": "2 pennies",
            "additional_info": "Good luck",
            "application_details": "Just come, no application required.",
        },
        {
            "type": PostType.OPEN_CALL,
            "title": "Rhythm Revue Casting",
            "organizer": "Martha Graham Dance Company",
            "closing_date": datetime.now(timezone.utc)
            + timedelta(days=random.randint(15, 130)),
            "tags": getRandVals(dance_tags),
            "location_type": LocationType.REMOTE,
            "location": "Zoom",
            "start_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(5, 15)),
            "end_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(17, 80)),
            "is_paid": False,
            "term_type": TermType.FULL_TIME,
            "number_positions": random.choice([None, 1, 2, 4, 8, 11]),
            "description": "We only accept the best.",
            "responsibilities": "Dance well",
            "requirements": "5 requirements, but we won't say what",
            "compensation": "You ain't getting nuffing.",
            "additional_info": "Good luck",
            "application_details": "Click the link below.",
            "application_link": "www.google.com",
        },
        {
            "type": PostType.AUDITION,
            "title": "Groove Gala Auditions",
            "organizer": "Royal Ballet",
            "closing_date": datetime.now(timezone.utc)
            + timedelta(days=random.randint(15, 130)),
            "tags": getRandVals(dance_tags),
            "location_type": LocationType.HYBRID,
            "location": random.choice(locations),
            "start_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(5, 15)),
            "end_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(17, 80)),
            "is_paid": True,
            "pay": "$983,249/minute",
            "term_type": TermType.PART_TIME,
            "number_positions": random.choice([None, 1, 2, 4, 8, 11]),
            "description": "Easy Audition",
            "requirements": "You must be the best dancer in Toronto.",
            "compensation": "A fortune.",
            "application_details": "Deposit $50,000 in the link below.",
            "application_link": "www.google.com",
        },
        {
            "type": PostType.INTENSIVE,
            "title": "Rhythm Rush Workshop",
            "organizer": "New York City Ballet",
            "closing_date": datetime.now(timezone.utc)
            + timedelta(days=random.randint(15, 130)),
            "tags": getRandVals(dance_tags),
            "location_type": LocationType.IN_PERSON,
            "location": random.choice(locations),
            "start_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(5, 15)),
            "is_paid": True,
            "pay": "$5.99 total",
            "number_positions": random.choice([None, 1, 2, 4, 8, 11]),
            "description": "Multi-week Intensive Program sure to get you a job anywhere!",
            "requirements": "None",
            "compensation": "~ 6 bucks.",
            "application_details": "Just come, no application required.",
        },
        {
            "type": PostType.DANCE_JOB,
            "title": "Ballet Instructor",
            "organizer": "National Ballet",
            "closing_date": datetime.now(timezone.utc)
            + timedelta(days=random.randint(15, 130)),
            "tags": getRandVals(dance_tags),
            "location_type": LocationType.IN_PERSON,
            "location": random.choice(locations),
            "start_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(5, 15)),
            "end_date": datetime.now(timezone.utc)
            + timedelta(weeks=random.randint(17, 80)),
            "is_paid": True,
            "pay": "$50,000 - $65,000 per year",
            "term_type": TermType.FULL_TIME,
            "number_positions": random.choice([None, 1, 2, 4, 8, 11]),
            "description": "Instruct future ballet geniuses to reach their full potential.",
            "responsibilities": "- Hold classes form 9am-3pm from Monday-Friday. \n- Record student progress weekly.\n- Report progress to the National Ballet",
            "requirements": "5 years of previous teaching experience of any genre of dance.",
            "compensation": "Starting from $50,000 per year but will increase up to 4x over the next 5 years.",
            "application_details": "Three round interview process. Further details in the link below",
            "application_link": "www.google.com",
        },
    ]

    users = db.session.query(User).all()
    for post in posts:
        create_opportunity_post(
            **post,
            poster_id=random.choice(users).id,
            display_description=post["description"]
        )

    db.session.commit()

    return redirect(url_for("opportunities.opportunities_list"))
