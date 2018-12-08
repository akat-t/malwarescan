#!/bin/sh
set -e

echo "Count: $#, Arguments passed: $@";
if [ "$#" -eq "0" ]; then
	echo "No command-line arguments supplied. Executing main supervisord routine... $ENV_TEST";
	exec supervisord -n -c contrib/super/superd.conf;
else
	echo "Command-line arguments supplied. Running them as /bin/bash -c ...";
	exec /bin/sh -c $@;
fi