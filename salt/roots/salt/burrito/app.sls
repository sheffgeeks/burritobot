include:
  - git
  - node
  - python3
  - python3.virtualenv

{{ pillar['installdir'] }}/burritoenv:
  virtualenv.managed:
    - requirements: {{ pillar['installdir'] }}/requirements.txt
    - python: /usr/bin/python3
    - runas: {{ pillar['user'] }}
    - require:
      - pkg: python3
      - pkg: python-virtualenv
      - pkg: git

install burritobot:
  cmd.run:
    - cwd: {{ pillar['installdir'] }}
    - user: {{ pillar['user'] }}
    - name: "{{ pillar['installdir'] }}/burritoenv/bin/python setup.py develop"
    - require:
      - virtualenv: {{ pillar['installdir'] }}/burritoenv

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
    - cwd: {{ pillar['installdir'] }}/scripts/js-sandbox
    - user: {{ pillar['user'] }}
    - require:
      - cmd: n stable

chicken-bin:
  pkg:
    - installed

chicken-sandbox-install:
  cmd.run:
    - name: chicken-install -sudo sandbox
    - cwd: {{ pillar['installdir'] }}
    - user: {{ pillar['user'] }}
    - require:
      - pkg: chicken-bin

csc-sandboxed:
  cmd.run:
    - name: csc scripts/scheme-sandbox/sandboxed.scm
    - cwd: {{ pillar['installdir'] }}
    - user: {{ pillar['user'] }}
    - require:
      - cmd: chicken-sandbox-install
