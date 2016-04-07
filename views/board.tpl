% def scripts():
    <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=all"></script>
    <script src="/js/whiteboard" async></script>
% end


% rebase('_base', title='Board ' + board.id, scripts=scripts)

<!-- 
<form>
    <label for="passphrase">Set a Passphrase:</label>
    <input type="text" placeholder="Passphrase" />
</form>
 -->

<svg id="board" xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600" data-boardid="{{board.id}}">

</svg>
