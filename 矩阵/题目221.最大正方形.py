# coding: utf-8           使用学习生长法进行思考，  认真开始分析，  题不在多，在于精

'''
      题目：在一个由 0 和 1 组成的二维矩阵内，找到只包含 1 的最大正方形，并返回其面积。

            示例
            输入:
            1 0 1 0 0
            1 0 1 1 1
            1 1 1 1 1
            1 0 0 1 0
            输出: 4

      分析：
            对矩阵里每个是1的元素（xi, yi），都进行搜索，

            以（xi, yi）为正方形左上角坐标，可能的正方形边长应该是 【1， min(m - i, n - j)】，

            为什么是【1， min(m - i, n - j)】？

            答：最小值显而易见是1；最大值因为是从左上角往右下画正方形，所以横边的长度最大为（n - i），
            竖边的长度最大为（m - i），接着尝试判断每一种正方形坐标范围内的点是否全为1。

      思路：

'''
class Solution(object):
    def maximalSquare(self, matrix):
        """
        :type matrix: List[List[str]]
        :rtype: int
        """
        m = len(matrix)
        if m == 0:
            return 0
        n = len(matrix[0])
        if n == 0:
            return 0
        self.res = 0

        def find(x, y):
            for length in range(1, min(m - i, n - j) + 1):  # length是边长
                cnt = 0

                for k in range(length):
                    for t in range(length):
                        xx = x + k
                        yy = y + t

                        if 0 <= xx < m and 0 <= yy < n:
                            if matrix[xx][yy] == "0":
                                return
                            else:
                                cnt += 1
                if cnt == length ** 2:
                    self.res = max(self.res, cnt)

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == "1":
                    find(i, j)

        return self.res

#___________________________________    练习1   ______________________________#
'''
   改题 选用 动态规划解法吧。

 状态设定：其中dp数组用来存储以第i行第j列元素为右下角的最大正方形的边长。仅当该位置为1时，才有可能存在正方形。
 
 状态转移：       
     （1）动态规划解题一般需要先构建一个dp数组，根据LeetCode官方解可以知道此问题的状态转移方程为：
             dp[i][j]=min(dp[i-1][j], dp[i-1][j-1], dp[i][j-1])+1，
     状态含义为若当前位置为1，则此处可以构成的最大正方形的边长，是其正上方，左侧，和左上界三者共同约束的，且为三者中的最小值加1。
     【注意当前位置为0时，其状态就是0，表示将当前点纳入到 最大正方形计算中。】
     （2）由于输入的矩阵为0-1矩阵，所以输入矩阵可以直接作为我们需要的dp数组，在遍历输入矩阵时可以按照上述状态转移公式原地更改矩阵。
  

   ——————————————————————————————————————————
   动态规矩，思路非常清晰，从左上 往 右下扫描即可。
   
  另一个比较好的说下：
    假设 f [ i ][ j ]是 以( i , j )为右下角的 最大正方形边长

    如果：（1）( i , j )位置为0，那么包含这个点的正方形都不符合条件（只包含 1），也就是说f [ i ][ j ]一定会等于0；
          （2）( i , j )位置为1，那么包含这个点的正方形的最大边长（即f [ i ][ j ]），应该考虑 左边相邻的点、上面相邻的点、左上方第一个点的最大正方形边长，即f [ i ][ j-1 ]、f [ i-1 ][ j ]、f [ i-1 ][ j-1 ]， 即f [ i ][ j ]=1+min( f [ i ][ j-1 ]，f [ i-1 ][ j ]，f [ i-1 ][ j-1 ])，为什么是取三个f中的最小值是因为，每个f代表对应的正方形，需要取这三个正方形的交集，才能把点( i , j )包含进去，这里不太好解释，可以自己画个图就清楚了。


     这个说的比较好，有三个理解的核心的吧：
        （1）一个是注意到， f [i][j]是指 以( i , j )为右下角的 最大正方形边长，并且 这个( i , j )位置必须在这个最大正方形中(必须是理解的核心)。所以当matrix[i][j]==0是，这个位置的状态值一定就是0.
        （2）第二就是 为什么要使用 左边相邻的点、上面相邻的点、左上方第一个点的最大正方形边长 三种中的最小值，是因为 这里每个f代表对应的正方形，需要取这三个正方形的交集，才能把点( i , j )包含进去。
          【画个图，就知道，简单的一个例子，比如 上边一个  左边一个 或者 左上边一个是0，那么现在这个铁定就是 0+1=1，以画下图就立马能明白了，0的阻断能力太强了。所以一定是最小的那个。】
        （3）我们是 收集最大的，所以 最右下方的matrix 值，并不会一定比matrix[1][1]的值，所以不要不要执着于变成 1或者0的影响。
   ——————————————————————————————————————————

'''
class Solution1:
    def maximalSquare(self, matrix):
        #  边界条件。 矩阵为空
        if not matrix:
            return 0

        # 针对正方形的每个位置，进行操作。  这里DP直接在本身操作，不单独进行状态的创建。  （res是现在知道的最大的正方形长度）
        res = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                #  针对于没1的位置，进行  状态转移操作
                if matrix[i][j] == '1':
                    matrix[i][j] = 1
                    # 单独对于 边界的位置做操作，不是一般的处理方式
                    if i == 0 or j == 0:
                        res = max(matrix[i][j], res)

                    # 非边界位置的处理。  使用状态转移方程
                    else:
                        #核心的  状态转移操作吧，   为什么是这三个位置 下的min呢？？？ 看最后的核心
                        matrix[i][j] = min(matrix[i-1][j], matrix[i-1][j-1], matrix[i][j-1])+1

                        res = max(matrix[i][j], res)
                else:
                    matrix[i][j] = 0
        return res**2


