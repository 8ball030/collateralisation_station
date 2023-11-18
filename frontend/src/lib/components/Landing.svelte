<script>
	$: bgImage = `
    background-image: url("/bg1.png");
    background-size: cover;
    background-position: center;
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;`;
	export let launch;
</script>

<div style={bgImage}>
	<div class="container h-full mx-auto flex justify-end items-center">
		<button class="btn variant-ringed-primary w-full mt-4 launch" on:click={launch}
			>Launch App</button
		>
	</div>
</div>

<style>
	.launch {
		width: 300px;
		margin-right: 190px;
	}
</style>
