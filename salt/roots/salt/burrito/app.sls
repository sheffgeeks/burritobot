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

/etc/burritobot:
  file.directory:
    - mode: 755

/etc/burritobot/burritobot.ini:
  file:
    - managed
    - source: salt://burrito/burritobot.ini
    - template: jinja
    - mode: 644

npm install:
  cmd.run:
    - cwd: /vagrant/scripts/js-sandbox
    - user: vagrant
    - require:
      - cmd: n stable

chicken-bin:
  pkg:
    - installed

chicken-sandbox-install:
  cmd.run:
    - name: chicken-install -sudo sandbox
    - cwd: /vagrant
    - user: vagrant
    - require:
      - pkg: chicken-bin

csc-sandboxed:
  cmd.run:
    - name: csc scripts/scheme-sandbox/sandboxed.scm
    - cwd: /vagrant
    - user: vagrant
    - require:
      - cmd: chicken-sandbox-install
