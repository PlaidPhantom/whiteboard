% def scripts():
    % # recommended by Bliss
    <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=all"></script>
    <script src="/js/index"></script>
% end

% rebase('_base', title='Home', scripts=scripts)

<header>
    <h1>Whiteboard</h1>
    <p>Collaborative brainstorming made easy.</p>
</header>

<main id="main">
    <form data-bind="submit: FindWhiteboard">
        <fieldset data-bind="css: idValid() ? 'valid' : 'error'">
            <label for="wb-id">Whiteboard ID:</label>
            <input type="text" id="wb-id" name="wb-id" placeholder="Whiteboard ID" data-bind="textInput: id" />
            <p><small>Only letters (A-Z, a-z), numbers (0-9), dashes (-), and underscores (_) allowed.</small></p>
        </fieldset>
        <button type="submit" data-bind="disable: !idValid() || searching()">Open Whiteboard</button>
    </form>

    <form data-bind="css: { show: confirmCreate }" class="confirm-create" method="post" action="/board/create">
        <input type="hidden" name="id" data-bind="value: id" />
        <p>That whiteboard currently doesn't exist.  Do you want to create it?</p>
        <button type="submit">Create</button>
    </form>

</main>
