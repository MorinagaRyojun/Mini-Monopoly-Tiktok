document.addEventListener('DOMContentLoaded', () => {
    const setupForm = document.getElementById('setup-form');

    if (setupForm) {
        setupForm.addEventListener('submit', handleSetupSubmit);
    }

    async function handleSetupSubmit(event) {
        event.preventDefault();

        const formData = new FormData(setupForm);
        const boardSize = formData.get('board_size');

        // Basic validation
        if (boardSize % 4 !== 0 || boardSize < 8) {
            alert('Board Size must be a multiple of 4 and at least 8.');
            return;
        }

        const imageUrls = {
            PROPERTY: formData.get('PROPERTY'),
            CHANCE: formData.get('CHANCE'),
            TAX: formData.get('TAX'),
            GO: formData.get('GO'),
            JAIL: formData.get('JAIL'),
            FREE_PARKING: formData.get('FREE_PARKING'),
            GO_TO_JAIL: formData.get('GO_TO_JAIL'),
        };

        // Filter out empty URLs
        const filteredImageUrls = Object.fromEntries(
            Object.entries(imageUrls).filter(([key, value]) => value !== '')
        );

        const payload = {
            board_size: parseInt(boardSize, 10),
            image_urls: filteredImageUrls,
        };

        console.log('Sending new game configuration:', payload);

        try {
            const response = await fetch('/api/new_game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                throw new Error('Failed to create new game.');
            }

            // On success, redirect back to the main game page
            window.location.href = '/';

        } catch (error) {
            console.error('Error creating new game:', error);
            alert('Could not start a new game. Please check the console for errors.');
        }
    }
});
