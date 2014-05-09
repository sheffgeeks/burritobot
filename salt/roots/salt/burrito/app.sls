include:
  - git
  - node
  - python3
  - python3.virtualenv

/home/vagrant/burritoenv:
  virtualenv.managed:
    - requirements: /vagrant/requirements.txt
    - python: /usr/bin/python3
    - runas: vagrant
    - require:
      - pkg: python3
      - pkg: python-virtualenv
      - pkg: git

install burritobot:
  cmd.run:
    - cwd: /vagrant
    - user: vagrant
    - name: "/home/vagrant/burritoenv/bin/python setup.py develop"
    - require:
      - virtualenv: /home/vagrant/burritoenv

/etc/burritobot/burritobot.ini:
  file:
    - managed
    - source: salt://burrito/burritobot.ini
    - template: jinja
    - mode: 644

npm install:
  cmd.run:
    - cwd: /vagrant/scripts/sandbox-cli
    - user: vagrant
    - require:
      - cmd: n stable
