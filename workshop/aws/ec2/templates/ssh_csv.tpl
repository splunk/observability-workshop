%{ for index, name in names ~}
${name}, ssh -p 2222 ubuntu@${ips[index]}, ${password}
%{ endfor ~}
