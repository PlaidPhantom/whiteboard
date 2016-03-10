#!/bin/bash

echo "Bundling $1..."

case "$1" in
    "js/index.bundle.js")
        echo ""                       >  js/index.bundle.js
        cat js/libs/knockout-3.4.0.js >> js/index.bundle.js
        echo ";"                      >> js/index.bundle.js
        cat js/libs/bliss.js          >> js/index.bundle.js
        echo ";"                      >> js/index.bundle.js
        cat js/index.js               >> js/index.bundle.js
        ;;
    "js/whiteboard.bundle.js")
        echo ""                >  js/whiteboard.bundle.js
        cat js/libs/bliss.js   >> js/whiteboard.bundle.js
        echo ";"               >> js/whiteboard.bundle.js
        cat js/SocketClient.js >> js/whiteboard.bundle.js
        echo ";"               >> js/whiteboard.bundle.js
        cat js/whiteboard.js   >> js/whiteboard.bundle.js
        ;;
    *)
        echo "Unknown target $1"
        exit 1
esac

exit 0
