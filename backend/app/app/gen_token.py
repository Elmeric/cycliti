# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
import secrets
import string
import base64


def main():
    # 24 8-bits utf-8 characters gives 4 * (24/3) 6-bits base64 encoded characters
    # token length will be 192 bits once encoded
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))
    encoded_token = base64.urlsafe_b64encode(token.encode()).decode()
    print(len(token), 8 * len(token), token)
    print(len(encoded_token), 6 * len(encoded_token), encoded_token)


if __name__ == '__main__':
    main()
