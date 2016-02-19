% rebase('_base', title='Home')

<header>
    <h1>Whiteboard</h1>
    <p>Collaborative brainstorming made easy.</p>
</header>

<main>
    <form action="/board/new" method="post">
        <label for="new-wb-id">Whiteboard ID:</label>
        <input type="text" id="new-wb-id" name="newid" />
        <br />
        <label for="new-pass">Passphrase:</label>
        <input type="text" id="new-pass" name="passphrase" />
        <br />
        <button type="submit">Create a new Whiteboard</button>
    </form>

    <form action="/board/join" method="post">
        <label for="wb-id">Whiteboard ID:</label>
        <input type="text" id="wb-id" name="id" />
        <button type="submit">Join a Whiteboard</button>
    </form>
</main>
