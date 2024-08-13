-- DB ����

CREATE DATABASE CO2

-- ������ Ȯ��
USE CO2
SELECT* FROM co2_generate
SELECT* FROM co2_absorb

-- co2_absorb�ǵ����͸� �õ���, ���س⵵ �������� �׷��Ͽ� �����հ�½ǰ���������� ���� ����Ͽ� ���ο� view�� ����
CREATE VIEW v_co2_abs AS (
	SELECT �õ���, ���س⵵, SUM(�����հ�½ǰ��������) AS �½ǰ��������
	FROM co2_absorb
	GROUP BY �õ���, ���س⵵
	)

SELECT * FROM v_co2_abs


-- co2_generate ���̺��� �ʿ��� �÷�(�����õ���, �⵵, ��ü�½ǰ������ⷮ)�� �����Ͽ� ���ο� veiw�� ����

CREATE VIEW v_co2_gen AS(
	SELECT �����õ���, �⵵, [��ü�½ǰ������ⷮ(tonCO2-eq)]
	FROM co2_generate
	)

SELECT * FROM v_co2_gen

-- v_co2_gen�� v_co2_abs�� �õ���/�⵵�� �������� ����
CREATE VIEW v_co2_neutral_ratio AS ( 
	SELECT
		a.�����õ��� AS �õ���,
		a.�⵵ AS �⵵,
		a.[��ü�½ǰ������ⷮ(tonCO2-eq)] AS �½ǰ������ⷮ,
		b.�½ǰ�������� AS �½ǰ��������,
		(b.�½ǰ��������/a.[��ü�½ǰ������ⷮ(tonCO2-eq)])*100 AS �½ǰ����߸���
	FROM v_co2_gen AS a
	INNER JOIN v_co2_abs AS b ON a.�����õ��� = b.�õ��� AND a.�⵵ = b.���س⵵
)

SELECT * FROM v_co2_neutral_ratio ORDER BY �õ���, �⵵

SELECT * FROM v_co2_neutral_ratio WHERE �⵵=2020 ORDER BY �½ǰ����߸���