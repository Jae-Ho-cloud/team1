-- DB 생성

CREATE DATABASE CO2

-- 데이터 확인
USE CO2
SELECT* FROM co2_generate
SELECT* FROM co2_absorb

-- co2_absorb의데이터를 시도명, 기준년도 기준으로 그룹하여 전국합계온실가스흡수량의 합을 계산하여 새로운 view로 저장
CREATE VIEW v_co2_abs AS (
	SELECT 시도명, 기준년도, SUM(전국합계온실가스흡수량) AS 온실가스흡수량
	FROM co2_absorb
	GROUP BY 시도명, 기준년도
	)

SELECT * FROM v_co2_abs


-- co2_generate 테이블에서 필요한 컬럼(광역시도명, 년도, 전체온실가스배출량)을 추출하여 새로운 veiw로 저장

CREATE VIEW v_co2_gen AS(
	SELECT 광역시도명, 년도, [전체온실가스배출량(tonCO2-eq)]
	FROM co2_generate
	)

SELECT * FROM v_co2_gen

-- v_co2_gen과 v_co2_abs를 시도명/년도를 기준으로 조인
CREATE VIEW v_co2_neutral_ratio AS ( 
	SELECT
		a.광역시도명 AS 시도명,
		a.년도 AS 년도,
		a.[전체온실가스배출량(tonCO2-eq)] AS 온실가스배출량,
		b.온실가스흡수량 AS 온실가스흡수량,
		(b.온실가스흡수량/a.[전체온실가스배출량(tonCO2-eq)])*100 AS 온실가스중립도
	FROM v_co2_gen AS a
	INNER JOIN v_co2_abs AS b ON a.광역시도명 = b.시도명 AND a.년도 = b.기준년도
)

SELECT * FROM v_co2_neutral_ratio ORDER BY 시도명, 년도

SELECT * FROM v_co2_neutral_ratio WHERE 년도=2020 ORDER BY 온실가스중립도