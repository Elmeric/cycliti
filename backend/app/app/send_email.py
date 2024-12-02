# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

from utils import verify_account_activation_nonce, send_account_activation_email


def main():
    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = "Ayons asperges pour le déjeuner"
    msg['From'] = Address("Pepé Le Pew", "pepe", "example.com")
    msg['To'] = (Address("Penelope Pussycat", "penelope", "example.com"),
                 Address("Fabrette Pussycat", "fabrette", "example.com"))
    msg.set_content("""
    Salut!

    Cela ressemble à un excellent recipie[1] déjeuner.

    [1] http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718

    --Pepé
    """)

    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    asparagus_cid = make_msgid()
    msg.add_alternative("""
    <html>
      <head></head>
      <body>
        <p>Salut!</p>
        <p>Cela ressemble à un excellent
            <a href="http://www.yummly.com/recipe/Roasted-Asparagus-Epicurious-203718">
                recipie
            </a> déjeuner.
        </p>
        <img src="cid:{asparagus_cid}" />
      </body>
    </html>
    """.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
    # note that we needed to peel the <> off the msgid for use in the html.

    # Now add the related image to the html part.
    with open("avatar-1.png", 'rb') as img:
        msg.get_payload()[1].add_related(img.read(), 'image', 'png',
                                         cid=asparagus_cid)

    with smtplib.SMTP(host="localhost", port=1025) as server:
        server.send_message(msg)


if __name__ == '__main__':
    send_account_activation_email(
        email_to="moi.nous@eux.fr",
        email="moi.nous@eux.fr",
        nonce="UnSuperJeton"
    )
    # email = verify_account_activation_token("3DeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV=CJ9.eyJleHAiOjE3MzIzMTg1MjYsIm5iZiI6MTczMjMxNDkyNiwic3ViIjoiZXJpay5sZW1vaW5lQ=GZyZWUuZnIifQ.ieRzSBILgg4urJM-KdBGzIEWJJ4Xhv2fkLXdiXC24G4")
    # print(email)
    # main()
