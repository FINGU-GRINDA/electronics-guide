import styles from './background.module.css';

export const Background = () => {
	return (
		<div className={styles.lines} style={{zIndex: -1}}>
			<div className={styles.line}></div>
			<div className={styles.line}></div>
			<div className={styles.line}></div>
		</div>
	);
};
