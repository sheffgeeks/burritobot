/usr/local/bin/n:
  file:
    - managed
    - source: https://raw.githubusercontent.com/visionmedia/n/a880cff47d831735de258256be39508a3250dacf/bin/n
    - source_hash: sha512=1d263b6f66468843ce960ed9ebdeed9ad314294b702a18b3dfd34f46dfd84b33e5b3e8227c1f9aa89708be1ec3eb47f4c603a7bfa26ff7814b3678d77d68eef9
    - mode: 751

curl:
  pkg:
    - installed

n stable:
  cmd.run:
    - user: root
    - require:
      - file: /usr/local/bin/n
      - pkg: curl
