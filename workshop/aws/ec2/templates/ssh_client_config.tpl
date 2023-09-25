Host *
  IdentitiesOnly yes
  PasswordAuthentication no
  PubkeyAuthentication yes
  ChallengeResponseAuthentication no
  CanonicalizeHostname yes
  StrictHostKeyChecking accept-new
  ForwardAgent no
%{ for index, name in names ~}
Host ${name}
    Hostname ${ips[index]}
    User ubuntu
    IdentityFile ${key}
%{ endfor ~}
