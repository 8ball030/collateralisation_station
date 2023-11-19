<script>
	export let value;
	export let onUserInput;

	function handleOnChange(event) {
		onUserInput(event.target.value);
	}
</script>

<input
	class="token-input"
	bind:value
	on:change={handleOnChange}
	type="text"
	pattern="^[0-9]*[.,]?[0-9]*$"
	minLength={1}
	maxLength={79}
/>

<style>
	.token-input {
		width: 0px;
		position: relative;
		font-weight: 500;
		outline: none;
		border: none;
		flex: 1 1 auto;
		background-color: transparent;
		font-size: 28px;
		overflow: hidden;
		text-overflow: ellipsis;
		text-align: left;
	}
</style>
