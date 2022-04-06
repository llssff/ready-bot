kill -9 $(ps | grep python3 | head -n1 | cut -f2 -d' ')
